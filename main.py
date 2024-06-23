import os
import docker
import subprocess
import tempfile
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import json

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

@app.get('/initial_code')
async def initial_code():
    with open('./initial_code.py', 'r') as f:
        code = f.read()
    return {"code": code}

class CodeInput(BaseModel):
    code: str

def create_script(code):
    # Escape any curly braces in the user's code
    escaped_code = code.replace("{", "{{").replace("}", "}}")
    
    return f"""
import sys
from io import StringIO
from contextlib import redirect_stdout
import json
import inspect

{escaped_code}

def run_solution():
    logged_output = StringIO()
    with redirect_stdout(logged_output):
        if 'Problem' in globals() and callable(globals()['Problem']):
            problem = Problem()
            if hasattr(problem, 'solution') and callable(problem.solution):
                # Check if solution method requires arguments
                sig = inspect.signature(problem.solution)
                if len(sig.parameters) > 0:
                    # If it requires arguments, we'll pass a default value of 2
                    return_output = problem.solution(2)
                    print(f"Result of solution(2): {{return_output}}")
                else:
                    return_output = problem.solution()
                    print(f"Result of solution(): {{return_output}}")
            else:
                print("No solution method found in Problem class or it's not callable")
                return_output = None
        else:
            print("No Problem class found or it's not callable")
            return_output = None
    
    return logged_output.getvalue().strip(), return_output

if __name__ == "__main__":
    logged_output, return_output = run_solution()
    print(logged_output)
    print(json.dumps({{"return_output": return_output}}))
"""

def run_code_locally(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(create_script(code))
        temp_file_path = temp_file.name

    try:
        result = subprocess.run(['python', temp_file_path], capture_output=True, text=True, timeout=30)
        
        # Split the output into lines
        output_lines = result.stdout.strip().split('\n') + result.stderr.strip().split('\n')
        
        # Try to parse the last line as JSON
        try:
            return_output = json.loads(output_lines[-1])['return_output']
            logged_output = '\n'.join(output_lines[:-1])
        except json.JSONDecodeError:
            # If parsing fails, treat everything as logged output
            logged_output = '\n'.join(output_lines)
            return_output = None
        
        return {
            "return_output": return_output,
            "logged_output": logged_output,
            "error": result.stderr if result.returncode != 0 else None
        }
    except subprocess.TimeoutExpired:
        raise Exception("Code execution timed out")
    finally:
        os.remove(temp_file_path)
        
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
                return_output = json.loads(output_lines[-1])['return_output']
                logged_output = '\n'.join(output_lines[:-1])
            except json.JSONDecodeError:
                logged_output = logs
                return_output = None
            
            return {
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
        "return_output": output["return_output"],
        "logged_output": output["logged_output"],
        "error": output.get("error")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)