test_case = [{
    'params': [[0,1,0,3,12]],
    'output': [1,3,12,0,0]
}]

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
                    input_data = test_case[0]['params']
                    output_data = test_case[0]['output']
                    return_output = problem.solution(*input_data)
                    valid = return_output == output_data
                    print(f"Expected Output: {input_data[0]}")
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
    
    print('return_output', return_output)
    return logged_output.getvalue().strip(), return_output, valid

if __name__ == "__main__":
    logged_output, return_output, valid = run_solution()
    print(logged_output)
    print(json.dumps({{"return_output": return_output, "valid": valid}}))