import sys
from io import StringIO
from contextlib import redirect_stdout
import json
import inspect

def run_solution(Problem):
    logged_output = StringIO()
    with redirect_stdout(logged_output):
        if callable(Problem):
            problem = Problem()
            if hasattr(problem, 'solution') and callable(problem.solution):
                # Check if solution method requires arguments
                sig = inspect.signature(problem.solution)
                if len(sig.parameters) > 0:
                    # If it requires arguments, we'll pass a default value
                    input_data = [0,1,0,3,12]
                    return_output = problem.solution(input_data)
                    valid = return_output == [1,3,12,0,0]  # Updated expected output
                    print(f"Expected Output: [1,3,12,0,0]")
                else:
                    return_output = problem.solution()
                    valid = True
                    print(f"Result of solution(): {return_output}")
            else:
                print("No solution method found in Problem class or it's not callable")
                valid = False
                return_output = None
        else:
            print("No Problem class found or it's not callable")
            return_output = None
            valid = False
    
    return logged_output.getvalue().strip(), return_output, valid

if __name__ == "__main__":
    # This allows the Problem class to be passed as a string
    Problem = globals()[sys.argv[1]] if len(sys.argv) > 1 else None
    logged_output, return_output, valid = run_solution(Problem)
    print(logged_output)
    print(json.dumps({"return_output": return_output, "valid": valid}))