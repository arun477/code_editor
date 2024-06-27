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
import shutil

DB_NAME = "problems_v8.db"
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
            f"SELECT * FROM {PROBLEM_TABLE} WHERE questionId = ?", (problem_id,)
        ).fetchone()


def get_all_problems():
    with create_sql_connection() as conn:
        cursor = conn.cursor()
        return cursor.execute("SELECT questionId,title from problems").fetchall()


app = FastAPI()
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

docker_client = docker.from_env()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/problem/{problem_id}", response_class=HTMLResponse)
async def problem_page(request: Request):
    return templates.TemplateResponse("problem.html", {"request": request})


@app.get("/all_problems")
async def get_all_problems_route():
    return {"problems": get_all_problems()}


@app.get("/problem_description/{problem_id}")
def get_problem_description(problem_id: str):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="not found")
    return {"description": problem["content"]}


@app.get("/initial_code/{problem_id}")
async def initial_code(problem_id: str):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="problem not found")
    return {"code": problem["initial_code"]}


@app.get("/get_problem/{problem_id}")
def get_problem_route(problem_id: str):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="not found")
    return problem


class RunCodeInput(BaseModel):
    problem_id: str
    code: str


def create_script(code, problem):
    executable_script = templates.get_template("execution_script_v3.jinja2").render(
        call_func=problem["call_func"], validation_func=problem["validation_func"], user_code=code
    )

    user_script = templates.get_template("user_code_template.jinja2").render(
        user_code=code
    )

    return (executable_script, user_script)


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


def create_temp_exection_files(executable_script, user_script, test_cases):
    temp_dir = tempfile.mkdtemp()
    with open(os.path.join(temp_dir, "execution_script.py"), "w") as dest:
        dest.write(executable_script)

    with open(os.path.join(temp_dir, "solution.py"), "w") as dest:
        dest.write(user_script)

    with open(os.path.join(temp_dir, "test_cases.json"), "w") as dest:
        test_cases = json.loads(test_cases)
        dest.write(json.dumps(test_cases))

    with open(os.path.join(temp_dir, "__init__.py"), "w") as dest:
        dest.write("")

    return temp_dir


def run_docker(code, problem_id):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="problem not found")
    
    problem = get_problem(problem_id)
    executable_script, user_script = create_script(code, problem)

    temp_dir = create_temp_exection_files(executable_script, user_script, problem['test_cases'])
    temp_dir_cache = tempfile.mkdtemp()

    with open("./temp.py", "w") as dest:
        dest.write(executable_script)

    with open(os.path.join(temp_dir_cache, "solution.py"), "w") as dest:
        dest.write(user_script)

    validation_config = {
        "image": "python:3.9-slim",
        "command": ["python", "-m", "py_compile", "/app-compile/solution.py"],
        "volumes": {
            temp_dir_cache: {"bind": "/app-compile", "mode": "rw"},
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
    try:
        with get_docker_container(container_config=validation_config) as container:
            exit_code = container.wait(timeout=10)["StatusCode"]
            if exit_code != 0:
                logs = container.logs(stdout=True, stderr=True).decode("utf-8")
                sanitized_error = str(logs)
                return {"outputs": {}, "error": sanitized_error}
    except OSError:
        return {
            "outputs": {},
            "error": "Permission denied",
        }
    except Exception as e:
        logger.exception("code execution failing", e)
        return {
            "outputs": {},
            "error": "An unexpected error occurred while running your code",
        }
    finally:
        shutil.rmtree(temp_dir_cache)
        pass

    container_config = {
        "image": "python:3.9-slim",
        "command": [
            "sh",
            "-c",
            "python /app/execution_script.py && mv /app/results.json /results/results.json",
        ],
        "volumes": {
            temp_dir: {"bind": "/app", "mode": "rw"},
            os.path.join(temp_dir, "results"): {"bind": "/results", "mode": "rw"},
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

    try:
        os.mkdir(os.path.join(temp_dir, "results"))

        with get_docker_container(container_config=container_config) as container:
            try:
                container.wait(timeout=30)
            except Exception as e:
                print('e...', e)
                return {"outputs": {}, "error": "Time Limit Exceeded"}

            logs = container.logs(stdout=True, stderr=True).decode("utf-8")

            if logs and logs.strip() == "Killed":
                return {
                    "outputs": {},
                    "error": "Memory Limit Exceeded",
                }
            print("logs:", logs)
            try:
                output_file_path = os.path.join(temp_dir, "results", "results.json")
                with open(output_file_path, "r") as file:
                    output = json.loads(file.read())

                if "error" in output:
                    return {"outputs": {}, "error": output["error"]}
                print('output:', output)
                return {"outputs": output, "logs": "", "error": None}
            except json.JSONDecodeError:
                return {
                    "outputs": {},
                    "logs": logs,
                    "error": "An unexpected error occurred while running your code. Logs",
                }
    except OSError as e:
        print(e)
        return {
            "outputs": {},
            "error": "Permission denied",
        }
    except Exception as e:
        logger.exception("code execution failing", e)
        return {
            "outputs": {},
            "error": "An unexpected error occurred while running your code",
        }
    finally:
        shutil.rmtree(temp_dir)


@app.post("/run_code")
def run_code(client_input: RunCodeInput):
    problem_id, code = client_input.problem_id, client_input.code
    result = run_docker(code, problem_id)
    return result or {}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
