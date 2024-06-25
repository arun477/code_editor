import sys
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import json
from typing import Any, List, Tuple, Dict, Set, Union, Optional, Callable
from user_script import *

def run_solution():
    results = []
    for test_case in [{'input': [[1, 2, 3, 4]], 'output': [24, 12, 8, 6]}, {'input': [[-1, 1, 0, -3, 3]], 'output': [0, 0, 9, 0, 0]}]:
        error = ""
        logged_output = StringIO()
        logged_error = StringIO()

        input_data = test_case['input']
        expected_output = test_case['output']
        return_output = None
        valid = None
        
        try:
            with redirect_stdout(logged_output), redirect_stderr(logged_error):
                return_output = Solution().productExceptSelf(*input_data)
                valid = return_output == expected_output

        except Exception as e:
            error = str(e)
        
        results.append({
            "input": input_data,
            "expected": expected_output,
            "output": return_output,
            "valid": valid,
            "error": error,
            "std_output": logged_output.getvalue().strip(),
            "std_error": logged_error.getvalue().strip()
        })
    return {"results": results}

if __name__ == "__main__":
    print(json.dumps(run_solution()))