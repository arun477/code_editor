import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic import BaseModel
import tempfile
import os
import json
import docker
import logging
import shutil
import uvicorn

DB_NAME = "problems_v9.db"
PROBLEM_TABLE = "problems"
SUBMISSION_TEST_CASE_TABLE = "submission_test_cases"


class DB:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn


@contextmanager
def create_sql_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        yield DB(cursor=conn.cursor(), conn=conn)
    finally:
        if conn:
            conn.close()


def get_problem(problem_id: str):
    with create_sql_connection() as _db:
        return _db.cursor.execute(
            f"SELECT * FROM {PROBLEM_TABLE} WHERE questionId = ?", (problem_id,)
        ).fetchone()


def get_all_problems():
    with create_sql_connection() as _db:
        return _db.cursor.execute(f"SELECT * FROM {PROBLEM_TABLE}").fetchall()


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
docker_client = docker.from_env()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/problem_page/{problem_id}", response_class=HTMLResponse)
async def problem_page(request: Request):
    return templates.TemplateResponse("problem.html", {"request": request})


@app.get("/get_problem/{problem_id}")
async def get_problem_route(problem_id: str):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="invalid problem id")
    return dict(problem)


@app.get("/all_problems")
async def get_all_problems_route():
    return {"problems": get_all_problems()}


def create_runnable_scripts(code, problem):
    exec_script = templates.get_template("execution_script_v2.jinja2").render(
        validation_func=problem
    )
    solution_script = templates.get_template("user_code_template.jinja2").render(
        user_code=code
    )
    return exec_script, solution_script


def temp_docker_mounting_folder(exec_script, solution_script, test_cases):
    temp_dir = tempfile.mkdtemp()
    with open(os.path.join(temp_dir, "execution_script.py"), "w") as dest:
        dest.write(exec_script)
    with open(os.path.join(temp_dir, "solution.py"), "w") as dest:
        dest.write(solution_script)
    with open(os.path.join(temp_dir, "test_cases.json"), "w") as dest:
        dest.write(json.dumps(json.loads(test_cases)))
    with open(os.path.join(temp_dir, "__init__.py"), "w") as dest:
        dest.write("")
    return temp_dir


@contextmanager
def get_new_docker_container(config):
    client = docker.from_env()
    container = None
    try:
        container = client.containers.run(**config)
    finally:
        if container:
            container.remove(force=True)


class DockerConfig:
    def __init__(self, volume_dir):
        self.DOCKER_CONFIG = {
            "image": "python:3.9-slim",
            "command": ["python", "-m", "py_compile", "/app-compile/solution.py"],
            "volumes": {
                volume_dir: {"bind": "/app-compile", "mode": "rw"},
            },
            "detach": True,
            "mem_limit": "250m",
            "cpu_quota": 50000,
            "network_mode": "none",
            "read_only": True,
            "user": "nobody",
            "pids_limit": 50,
            "security_opt": ["no-new-privileges"],
        }
        return self.DOCKER_CONFIG


def run_code_validation(temp_dir):
    docker_config = DockerConfig(volume_dir=temp_dir)
    try:
        with get_new_docker_container(docker_config) as container:
            exit_code = container.wait(timeout=10)["StatusCode"]
            if exit_code != 0:
                logs = container.logs(stdout=True, stderr=True).decode("utf-8")
                return {"outputs": {}, "error": str(logs)}
    except OSError:
        return {"outputs": {}, "error": "permission denied"}
    except Exception as _:
        return {"outputs": {}, "error": "an unexpected error occured"}
    return None


def run_user_solution_code(temp_dir):
    docker_config = DockerConfig(volume_dir=temp_dir)
    try:
        with get_new_docker_container(docker_config) as container:
            try:
                container.wait(timeout=30)
            except Exception as _:
                return {"outputs": {}, "error": "time limit exceeded"}
            logs = container.logs(stdout=True, stderr=True).decode("utf-8")
            if logs and logs.strip() == "Killed":
                return {"outputs": {}, "error": "memory limit exceeded"}

            output_file_path = os.path.join(temp_dir, "results", "results.json")
            with open(output_file_path, "r") as file:
                output = json.loads(file.read())
            return {"outputs": output, "logs": "", "error": output.get("error", None)}
    except OSError:
        return {"outputs": {}, "error": "permission denied"}
    except Exception as _:
        return {"outputs": {}, "error": "an unexpected error occured"}


def remove_temp_dir(temp_dir):
    try:
        shutil.rmtree(temp_dir)
    except Exception as _:
        pass


def run_in_docker(code, problem):
    exec_script, solution_script = create_runnable_scripts(code, problem)
    temp_dir = temp_docker_mounting_folder(
        exec_script, solution_script, problem["test_cases"]
    )

    failed_validation = run_code_validation(temp_dir)
    if failed_validation:
        return failed_validation

    execution_output = run_user_solution_code(temp_dir)
    remove_temp_dir(temp_dir)

    return execution_output


class RunCodeInput(BaseModel):
    problem_id: str
    code: str


@app.post("/run_code")
async def run_code(run_code_input: RunCodeInput):
    problem_id, code = run_code_input.problem_id, run_code_input.code
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="invalid problem id")
    result = run_in_docker(code, problem)
    return result or {}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
