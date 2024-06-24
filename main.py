import os
import docker
import tempfile
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import json
import sqlite3
from contextlib import contextmanager

# Database setup
DATABASE_NAME = "problems_v2.db"


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def get_problem(problem_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM problems WHERE id = ?", (problem_id,))
        return cursor.fetchone()


# FastAPI setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")
client = docker.from_env()

# Logging setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/problem_description/{problem_id}")
async def problem_description(problem_id: str):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return {"description": problem["problem_statement"]}


@app.get("/get_problem/{problem_id}")
async def get_problem_route(problem_id: str):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@app.get("/initial_code/{problem_id}")
async def initial_code(problem_id: str):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return {"code": problem["starting_code"]}


class CodeInput(BaseModel):
    code: str
    problem_id: str


def create_script(code, problem_id):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    test_cases = json.loads(problem["test_cases"])

    execution_template = """
import sys
from io import StringIO
from contextlib import redirect_stdout
import json
import inspect

{USER_EXECUTION_CODE}         

def run_solution():
    logged_output = StringIO()
    with redirect_stdout(logged_output):
        results = []
        for test_case in {TEST_CASES}:
            input_data = test_case['input']
            expected_output = test_case['output']
            try:
                return_output = Problem().solution(*input_data)
                valid = return_output == expected_output
            except Exception as e:
                return_output = str(e)
                valid = False
            results.append({{"input": input_data, "expected": expected_output, "output": return_output, "valid": valid}})
        
        all_valid = all(result['valid'] for result in results)
        print("Tests {{}}".format('Passed' if all_valid else 'Failed'))
    
    return logged_output.getvalue().strip(), results, all_valid

if __name__ == "__main__":
    logged_output, results, all_valid = run_solution()
    print(logged_output)
    print(json.dumps({{"results": results, "all_valid": all_valid}}))
"""

    return execution_template.format(
        USER_EXECUTION_CODE=code, TEST_CASES=json.dumps(test_cases)
    )


def run_code_in_docker(code, problem_id):
    client = docker.from_env()
    temp_dir = tempfile.mkdtemp()

    try:
        script_content = create_script(code, problem_id)
        with open(os.path.join(temp_dir, "script.py"), "w") as f:
            f.write(script_content)

        container = client.containers.run(
            "python:3.9-slim",
            ["python", "/app/script.py"],
            volumes={temp_dir: {"bind": "/app", "mode": "ro"}},
            detach=True,
            mem_limit="100m",
            cpu_quota=50000,
            network_mode="none",
            read_only=True,
        )

        try:
            result = container.wait(timeout=30)
            logs = container.logs(stdout=True, stderr=True).decode("utf-8")

            output_lines = logs.strip().split("\n")

            try:
                output = json.loads(output_lines[-1])
                results = output["results"]
                all_valid = output["all_valid"]
                logged_output = "\n".join(output_lines[:-1])
            except json.JSONDecodeError:
                logged_output = logs
                results = None
                all_valid = False

            return {
                "all_valid": all_valid,
                "results": results,
                "logged_output": logged_output,
                "error": logs if result["StatusCode"] != 0 else None,
            }
        finally:
            container.remove(force=True)
    except Exception as e:
        logger.exception("Error in Docker execution")
        return {
            "all_valid": False,
            "results": None,
            "logged_output": None,
            "error": str(e),
        }
    finally:
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)


@app.post("/run_code")
async def run_code(code_input: CodeInput):
    code = code_input.code
    problem_id = code_input.problem_id

    try:
        output = run_code_in_docker(code, problem_id)
        logger.info("Code executed successfully")
    except HTTPException as http_error:
        # Re-raise HTTP exceptions (like 404 Not Found)
        raise http_error
    except Exception as docker_error:
        logger.exception(f"Failed to run: {str(docker_error)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(docker_error)}"
        )

    if output.get("error"):
        logger.warning(f"Code execution produced an error: {output['error']}")
        return {
            "all_valid": False,
            "results": [],
            "logged_output": output["error"],
            "error": output["error"],
        }

    return {
        "all_valid": output["all_valid"],
        "results": output["results"],
        "logged_output": output["logged_output"],
        "error": output.get("error"),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)