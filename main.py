import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic import BaseModel, field_validator
import logging
import docker
import tempfile
import os
import json
import shutil
import ast

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

    problem = dict(problem)
    return problem


class ProblemUpdate(BaseModel):
    title: str
    content: str
    initial_code: str
    validation_func: str
    test_cases: str

    @field_validator("initial_code")
    @classmethod
    def validate_initial_code(cls, v):
        try:
            tree = ast.parse(v)
            classes = [
                node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
            ]
            if not any(cls.name == "Solution" for cls in classes):
                raise ValueError("Initial code must contain a Solution class")
        except SyntaxError:
            raise ValueError("Invalid Python syntax in initial code")
        return v

    @field_validator("validation_func")
    @classmethod
    def validate_validation_func(cls, v):
        try:
            tree = ast.parse(v)
            classes = [
                node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
            ]
            if not any(cls.name == "Validation" for cls in classes):
                raise ValueError("Validation function must contain a Validation class")

            validation_class = next(cls for cls in classes if cls.name == "Validation")
            methods = [
                node
                for node in validation_class.body
                if isinstance(node, ast.FunctionDef)
            ]
            if not any(method.name == "main" for method in methods):
                raise ValueError("Validation class must contain a 'main' method")

            # Check if the main method returns a tuple
            main_method = next(method for method in methods if method.name == "main")
            returns = [
                node for node in ast.walk(main_method) if isinstance(node, ast.Return)
            ]
            if not returns or not isinstance(returns[0].value, ast.Tuple):
                raise ValueError("The 'main' method must return a tuple")

            if len(returns[0].value.elts) != 2:
                raise ValueError("The 'main' method")
        except SyntaxError:
            raise ValueError("Invalid Python syntax in validation function")
        return v

    @field_validator("test_cases")
    @classmethod
    def validate_test_cases(cls, v):
        try:
            cases = json.loads(v)
            if not isinstance(cases, list) or len(cases) == 0:
                for case in cases:
                    if (
                        not isinstance(case, dict)
                        or "input" not in case
                        or "expected" not in case
                    ):
                        raise ValueError(
                            "Each test case must be a dictionary with 'input' and 'expected' keys"
                        )
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in test cases")
        return v


@app.put("/admin/update-problem/{problem_id}")
async def update_problem(problem_id: str, problem_update: ProblemUpdate):
    with create_sql_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
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
            conn.commit()
            return {"message": "Problem updated successfully"}
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# @app.put("/admin/update-problem/{problem_id}")
# async def update_problem(problem_id: str, problem_update: ProblemUpdate):
#     with create_sql_connection() as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute(
#                 f"""
#                 UPDATE {PROBLEM_TABLE}
#                 SET title = ?, content = ?, initial_code = ?, validation_func = ?, test_cases = ?
#                 WHERE questionId = ?
#                 """,
#                 (
#                     problem_update.title,
#                     problem_update.content,
#                     problem_update.initial_code,
#                     problem_update.validation_func,
#                     problem_update.test_cases,
#                     problem_id,
#                 ),
#             )
#             conn.commit()
#             return {"message": "Problem updated successfully"}
#         except sqlite3.Error as e:
#             raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/admin/edit-problem/{problem_id}", response_class=HTMLResponse)
def edit_problem_page(request: Request):
    return templates.TemplateResponse("edit_problem.html", {"request": request})


class RunCodeInput(BaseModel):
    problem_id: str
    code: str


def create_script(code, problem):
    executable_script = templates.get_template("execution_script_v2.jinja2").render(
        call_func=problem["call_func"],
        validation_func=problem["validation_func"],
        user_code=code,
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

    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".py", delete=False
    ) as exec_script_file:
        exec_script_file.write(executable_script)
        exec_script_path = exec_script_file.name

    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".py", delete=False
    ) as user_script_file:
        user_script_file.write(user_script)
        user_script_path = user_script_file.name

    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".json", delete=False
    ) as test_cases_file:
        test_cases = json.loads(problem["test_cases"])
        json.dump(test_cases, test_cases_file)
        test_cases_path = test_cases_file.name

    results_dir = tempfile.mkdtemp()

    temp_dir = create_temp_exection_files(
        executable_script, user_script, problem["test_cases"]
    )
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
            temp_dir: {"bind": "/app", "mode": "ro"},
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
                print("e...", e)
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
                print("output:", output)
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
