import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic import BaseModel, field_validator
import tempfile
import os
import json
import docker
import logging
import shutil
import uvicorn
import ast
import redis
import concurrent.futures
import time
import psutil

DB_NAME = "problems_v9.db"
PROBLEM_TABLE = "problems"
SUBMISSION_TEST_CASE_TABLE = "submission_test_cases"

redis_client = redis.Redis(host="localhost", port=6379, db=0)


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


def get_submission_test_cases(problem_id: str):
    with create_sql_connection() as _db:
        return _db.cursor.execute(
            f"SELECT * FROM {SUBMISSION_TEST_CASE_TABLE} WHERE questionId = ?",
            (problem_id,),
        ).fetchall()


def admin_update_problem(problem_id: str, problem_update):
    with create_sql_connection() as _db:
        try:
            _db.cursor.execute(
                f"""
                UPDATE {PROBLEM_TABLE}
                SET title = ?, content = ?, initial_code = ?, validation_func = ?, test_cases = ?
                WHERE questionId = ?
                """,
                (
                    problem_update.title,
                    problem_update.content,
                    problem_update.initial_code,
                    problem_update.validation_func,
                    problem_update.test_cases,
                    problem_id,
                ),
            )
            _db.conn.commit()
        except sqlite3.Error as _:
            raise HTTPException(status_code=500, detail="invalid update data")


app = FastAPI()
templates = Jinja2Templates(directory="templates")
docker_client = docker.from_env()


def create_runnable_scripts(code, problem):
    exec_script = templates.get_template("execution_script.jinja2").render(
        validation_func=problem["validation_func"]
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
    os.mkdir(os.path.join(temp_dir, "results"))
    return temp_dir


@contextmanager
def get_new_docker_container(config):
    client = docker.from_env()
    container = None
    try:
        container = client.containers.run(**config)
        yield container
    finally:
        if container:
            container.remove(force=True)


class DockerConfig:
    def __init__(self, volume_dir, env="validation", cmd_on=True):
        if env == "validation":
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
        elif env == "execution":
            self.DOCKER_CONFIG = {
                "image": "python:3.9-slim",
                "command": [
                    "sh",
                    "-c",
                    "python /app/execution_script.py",
                ]
                if cmd_on
                else [
                    "tail",
                    "-f",
                    "/dev/null",
                ],
                "volumes": {
                    volume_dir: {"bind": "/app", "mode": "ro"},
                    os.path.join(volume_dir, "results"): {
                        "bind": "/results",
                        "mode": "rw",
                    },
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


def run_code_validation(temp_dir):
    docker_config = DockerConfig(volume_dir=temp_dir, env="validation").DOCKER_CONFIG
    try:
        with get_new_docker_container(config=docker_config) as container:
            exit_code = container.wait(timeout=10)["StatusCode"]
            if exit_code != 0:
                logs = container.logs(stdout=True, stderr=True).decode("utf-8")
                return {"outputs": {}, "error": str(logs)}
    except OSError as _:
        return {"outputs": {}, "error": "permission denied"}
    except Exception as _:
        return {"outputs": {}, "error": "an unexpected error occured"}
    return None


def handle_execution_run(container, temp_dir, is_submission=False):
    if not is_submission:
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


def run_user_solution_code(temp_dir):
    docker_config = DockerConfig(volume_dir=temp_dir, env="execution").DOCKER_CONFIG
    try:
        with get_new_docker_container(config=docker_config) as container:
            return handle_execution_run(container, temp_dir)
    except OSError as _:
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
        remove_temp_dir(temp_dir)
        return failed_validation

    execution_output = run_user_solution_code(temp_dir)
    remove_temp_dir(temp_dir)

    return execution_output


def submit_in_docker(code, problem):
    submission_test_cases = [
        dict(ele) for ele in get_submission_test_cases(problem["questionId"])
    ]
    exec_script, solution_script = create_runnable_scripts(code, problem)
    temp_dir = temp_docker_mounting_folder(
        exec_script, solution_script, problem["test_cases"]
    )

    failed_validation = run_code_validation(temp_dir)
    if failed_validation:
        remove_temp_dir(temp_dir)
        return failed_validation

    docker_config = DockerConfig(
        volume_dir=temp_dir, env="execution", cmd_on=False
    ).DOCKER_CONFIG
    output = None
    error = None
    with get_new_docker_container(config=docker_config) as container:
        passed_test_cases = 0
        for test_case in submission_test_cases:
            with open(os.path.join(temp_dir, "test_cases.json"), "w") as dest:
                dest.write(json.dumps([json.loads(test_case["test_case"])]))

            exit_code, output = container.exec_run(
                cmd=[
                    "sh",
                    "-c",
                    "python /app/execution_script.py",
                ],
                user="nobody",
            )
            output = handle_execution_run(container, temp_dir, is_submission=True)[
                "outputs"
            ]["results"][0]
            if output["error"]:
                error = output["error"]
                break
            if output and output.get("valid"):
                passed_test_cases = passed_test_cases + 1
            else:
                return {
                    "output": {
                        "passed": passed_test_cases,
                        "total": len(submission_test_cases),
                    },
                    "logs": output,
                }

    remove_temp_dir(temp_dir)

    return {
        "output": {"passed": passed_test_cases, "total": len(submission_test_cases)},
        "error": error,
    }


def set_job_status(job_id, job_status):
    redis_client.set(f"jobs:{job_id}", json.dumps(job_status))


def process_job(job_data):
    run_code_input = job_data["run_code_input"]
    job_id = job_data["job_id"]
    problem_id, code = run_code_input["problem_id"], run_code_input["code"]
    problem = get_problem(problem_id)
    set_job_status(job_id, {"status": "pending", "result": None})

    if job_data["job_type"] == "run":
        result = run_in_docker(code, problem)
    else:
        result = submit_in_docker(code, problem)

    set_job_status(job_id, {"status": "done", "result": result})


def execute_docker_job(job_data):
    run_code_input = job_data["run_code_input"]
    job_id = job_data["job_id"]
    problem_id, code = run_code_input["problem_id"], run_code_input["code"]
    problem = get_problem(problem_id)
    set_job_status(job_id, {"status": "pending", "result": None})

    if job_data["job_type"] == "run":
        result = run_in_docker(code, problem)
    else:
        result = submit_in_docker(code, problem)

    set_job_status(job_id, {"status": "done", "result": result})


def process_jobs():
    redis_client = redis.Redis(host="localhost", port=6379, db=0)

    # Determine the number of physical cores
    physical_cores = psutil.cpu_count(logical=False)

    # Set max_workers to the number of physical cores
    max_worker = physical_cores

    print(f"Using {max_worker} workers based on available physical cores")

    # max_worker = 15

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
        while True:
            try:
                # Fetch multiple jobs at once (up to 4)
                pipe = redis_client.pipeline()
                pipe.lrange("code_execution_queue", 0, max_worker - 1)
                pipe.ltrim("code_execution_queue", max_worker, -1)
                results = pipe.execute()
                jobs = results[0]

                if not jobs:
                    # If no jobs, wait for a short time before checking again
                    time.sleep(0.1)
                    continue

                # Process the jobs concurrently
                job_data_list = [json.loads(job) for job in jobs]
                list(executor.map(execute_docker_job, job_data_list))

            except Exception as e:
                print(f"Error in process_jobs: {e}")


if __name__ == "__main__":
    process_jobs()
