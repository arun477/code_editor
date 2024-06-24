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

DATABASE_NAME = "problems.db"

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    try:
        yield conn
    finally:
        conn.close()


def get_problem(problem_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM problems WHERE id = ?', (problem_id,))
        return cursor.fetchone()


app = FastAPI()
templates = Jinja2Templates(directory="templates")
client = docker.from_env()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/problem_description/{problem_id}')
async def problem_description(problem_id:str):
    description = get_problem(problem_id)['problem_statement']
    return {"description": description}

@app.get('/initial_code/{problem_id}')
async def initial_code(problem_id:str):
    code = get_problem(problem_id)['starting_code']
    return {"code": code}

class CodeInput(BaseModel):
    code: str


def create_script(code):
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
        valid = False
        return_output = None
        {PROBLEM_SPECIFIC_CODE}
    
    return logged_output.getvalue().strip(), return_output, valid

if __name__ == "__main__":
    logged_output, return_output, valid = run_solution()
    print(logged_output)
    print(json.dumps({{"return_output": return_output, "valid": valid}}))"""

    # Escape any curly braces in the user's code
    escaped_code = code.replace("{", "{{").replace("}", "}}")

    PROBLEM_SPECIFIC_CODE = """
        input_data = [0, 1, 0, 3, 12]
        return_output = Problem().solution(input_data)
        expected_output = [1, 3, 12, 0, 0]  # Assuming the problem is to move zeroes to the end
        valid = return_output == expected_output
        print("Input: " + str(input_data))
        print("Expected Output: " + str(expected_output))
        print("Your Output: " + str(return_output))
    """
    return execution_template.format(USER_EXECUTION_CODE=escaped_code, PROBLEM_SPECIFIC_CODE=PROBLEM_SPECIFIC_CODE)

def run_code_in_docker(code):
    client = docker.from_env()
    temp_dir = tempfile.mkdtemp()

    try:
        with open(os.path.join(temp_dir, "script.py"), "w") as f:
            f.write(create_script(code))

        container = client.containers.run(
            "python:3.9-slim",
            ["python", "/app/script.py"],
            volumes={temp_dir: {'bind': '/app', 'mode': 'ro'}},
            detach=True,
            mem_limit="100m",
            cpu_quota=50000,
            network_mode="none",
            read_only=True,
        )
        
        try:
            result = container.wait(timeout=30)
            logs = container.logs(stdout=True, stderr=True).decode('utf-8')
            
            output_lines = logs.strip().split('\n')
            
            try:
                output = json.loads(output_lines[-1])
                return_output = output['return_output']
                valid = output['valid']
                logged_output = '\n'.join(output_lines[:-1])
            except json.JSONDecodeError:
                logged_output = logs
                return_output = None
                valid = False
            
            return {
                'valid': valid,
                "return_output": return_output,
                "logged_output": logged_output,
                "error": logs if result['StatusCode'] != 0 else None
            }
        finally:
            container.remove(force=True)
    except Exception as e:
        logger.exception("Error in Docker execution")
        raise
    finally:
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

@app.post("/run_code")
async def run_code(code_input: CodeInput):
    code = code_input.code
    
    output = {}
    try:
        output = run_code_in_docker(code)
        logger.info("Code executed successfully in Docker")
    except Exception as docker_error:
        logger.warning(f"Failed to run in Docker: {str(docker_error)}. Falling back to local execution.")
        # try:
        #     output = run_code_locally(code)
        #     logger.info("Code executed successfully locally")
        # except Exception as local_error:
        #     logger.exception("Local execution also failed")
        #     raise HTTPException(status_code=400, detail=str(local_error))

    if output.get("error"):
        logger.warning(f"Code execution produced an error: {output['error']}")
  
    return {
        "valid": output["valid"],
        "return_output": str(output["return_output"]),
        "logged_output": output["logged_output"],
        "error": output.get("error")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)