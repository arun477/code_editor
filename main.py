import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic import BaseModel
import logging
import docker
import tempfile
import os
import json


DB_NAME = "problems_v2.db"
PROBLEM_TABLE = "problems"


@contextmanager
def create_sql_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        conn.close()


def get_problem(problem_id: str):
    with create_sql_connection() as conn:
        cursor = conn.cursor()
        return cursor.execute(
            f"SELECT * FROM {PROBLEM_TABLE} WHERE id = ?", (problem_id)
        ).fetchone()


app = FastAPI()
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

docker_client = docker.from_env()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/problem_description/{problem_id}")
def get_problem_description(problem_id: str):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="not found")
    return {"description": problem["problem_statement"]}


@app.get("/initial_code/{problem_id}")
async def initial_code(problem_id: str):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="problem not found")
    return {"code": problem["starting_code"]}


@app.get("/get_problem/{problem_id}")
def get_problem_route(problem_id: str):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="not found")
    return problem


class RunCodeInput(BaseModel):
    problem_id: str
    code: str


def create_script(code, problem_id):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="problem not found")
    test_cases = json.loads(problem["test_cases"])

    return templates.get_template("execution_script.jinja2").render(
        user_code=code, test_cases=test_cases
    )


@contextmanager
def get_docker_container(container_config):
    client = docker.from_env()
    container = None
    try:
        container = client.containers.run(**container_config)
        yield container
    finally:
        if container:
            container.remove(force=True)


def run_docker(code, problem_id):
    temp_dir = tempfile.mkdtemp()

    executable_script = create_script(code, problem_id)
    with open(os.path.join(temp_dir, "script.py"), "w") as dest:
        dest.write(executable_script)

    container_config = {
        "image": "python:3.9-slim",
        "command": ["python", "/app/script.py"],
        "volumes": {
            temp_dir: {"bind": "/app", "mode": "ro"},
        },
        "detach": True,
        "mem_limit": "100m",
        "cpu_quota": 50000,
        "network_mode": "none",
        "read_only": True,
    }

    try:
        with get_docker_container(container_config=container_config) as container:
            container.wait(timeout=30)
            logs = container.logs(stdout=True, stderr=True).decode("utf-8")
            try:
                output = json.loads(logs)
                if "error" in output:
                    return {"outputs": {}, "error": output["error"]}
                return {"outputs": output, "logs": "", "error": None}
            except json.JSONDecodeError:
                return {
                    "outputs": {},
                    "logs": logs,
                    "error": f"An unexpected error occurred while running your code. Logs: {logs}",
                }
    except Exception as e:
        logger.exception("code execution failing", e)
        return {
            "outputs": {},
            "error": "An unexpected error occurred while running your code.",
        }
    finally:
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)


@app.post("/run_code")
def run_code(client_input: RunCodeInput):
    problem_id, code = client_input.problem_id, client_input.code
    result = run_docker(code, problem_id)
    return result or {}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
