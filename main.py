from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import StringIO
from contextlib import redirect_stdout
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import ast
import builtins

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class CodeInput(BaseModel):
    code: str

def is_safe_ast(node):
    """Check if the AST node is safe to execute."""
    # Blacklist of dangerous operations
    dangerous_calls = {'eval', 'exec', 'compile', 'open', '__import__'}
    
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in dangerous_calls:
            return False
        if isinstance(node.func, ast.Attribute) and node.func.attr in dangerous_calls:
            return False
    
    # Recursively check all child nodes
    for child in ast.iter_child_nodes(node):
        if not is_safe_ast(child):
            return False
    
    return True

def safe_exec(code, global_dict, local_dict):
    """Safely execute code after checking its AST."""
    try:
        tree = ast.parse(code)
        if not is_safe_ast(tree):
            raise ValueError("Unsafe operations detected in the code")
        
        compiled_code = compile(tree, "<string>", "exec")
        exec(compiled_code, global_dict, local_dict)
    except Exception as e:
        raise ValueError(f"Error executing code: {str(e)}")

@app.post("/run_code")
async def run_code(code_input: CodeInput):
    code = code_input.code
    
    # Use StringIO and redirect_stdout to capture print statements
    output = StringIO()
    
    try:
        # Create a restricted global namespace
        safe_globals = {
            "__builtins__": {
                name: getattr(builtins, name)
                for name in dir(builtins)
                if name not in ['eval', 'exec', 'compile', 'open', '__import__']
            }
        }
        
        # Create a local namespace for execution
        local_namespace = {}
        
        # Execute the code and capture print output
        with redirect_stdout(output):
            safe_exec(code, safe_globals, local_namespace)
            
            # Explicitly call the solution function if it exists
            if 'solution' in local_namespace and callable(local_namespace['solution']):
                result = local_namespace['solution'](2)  # Assuming solution takes one argument
                print(f"Result of solution(2): {result}")
            else:
                print("No solution function found or it's not callable")
                result = None

        # Get the print output
        print_output = output.getvalue()
        
        return {
            "print_output": print_output,
            "return_output": str(result) if result is not None else "No result"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)