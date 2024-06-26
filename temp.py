import multiprocessing
import psutil
import os
import signal
import time
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import json
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import json
import traceback
from user_script import *

def monitor_process_func(
    pid, allowed_memory_bytes, start_time, allowed_time_sec, msg_queue
):
    try:
        process = psutil.Process(pid)
        while True:
            try:
                time_elapsed = time.time() - start_time
                if time_elapsed >= allowed_time_sec:
                    os.kill(pid, signal.SIGTERM)
                    msg_queue.put(("TimeLimitExceeded", None))
                    return

                mem_info = process.memory_info()
                if mem_info.rss >= allowed_memory_bytes:
                    os.kill(pid, signal.SIGTERM)
                    msg_queue.put(("MemoryLimitExceeded", None))
                    return

            except psutil.NoSuchProcess:
                return
            time.sleep(0.1)
    except Exception as e:
        msg_queue.put(("MonitorException", str(e)))


def execution_func(test_case, msg_queue):
    error = ""
    logged_output = StringIO()
    logged_error = StringIO()

    input_data = test_case["input"]
    expected_output = test_case["output"]
    return_output = None
    valid = None
    try:
        with redirect_stdout(logged_output), redirect_stderr(logged_error):
            return_output = Solution().gcdOfStrings(*input_data)
            valid = return_output == expected_output
        msg_queue.put(
                (
                    "result",
                    json.dumps({
                        "input": input_data,
                        "expected": expected_output,
                        "output": return_output,
                        "valid": valid,
                        "error": error,
                        "std_output": logged_output.getvalue().strip(),
                        "std_error": logged_error.getvalue().strip(),
                    }),
                )
            )
    except Exception as e:
        error = str(e)
        msg_queue.put(
           (
                "CodeException",
                json.dums( {
                    "input": input_data,
                    "expected": expected_output,
                    "output": return_output,
                    "valid": valid,
                    "error": error,
                    "std_output": '',
                    "std_error": '',
                }),
            )
        )


class MemoryLimitExceeded(Exception):
    pass


class TimeLimitExceeded(Exception):
    pass


def execute(test_case, allowed_memory_bytes=1, allowed_time_sec=10, *args, **kwargs):
    msg_queue = multiprocessing.Queue()
    start_time = time.time()
    code_execution_process = multiprocessing.Process(
        target=execution_func, args=(test_case, args, kwargs, msg_queue)
    )
    code_execution_process.start()

    monitor_process = multiprocessing.Process(
        target=monitor_process_func,
        args=(
            code_execution_process.pid,
            allowed_memory_bytes * 1024 * 1024,
            start_time,
            allowed_time_sec,
            msg_queue,
        ),
    )
    monitor_process.start()

    try:
        status, msg = msg_queue.get(timeout=allowed_time_sec + 1)
        if status == "TimeLimitExceeded":
            raise TimeLimitExceeded("TimeLimitExceeded")
        if status == "MemoryLimitExceeded":
            raise MemoryLimitExceeded("MemoryLimitExceeded")
        elif status == "CodeException":
            return msg
        elif status == "MonitorException":
            raise Exception(msg)
        return msg
    except Exception as e:
        raise TimeoutError(e)
    finally:
        code_execution_process.terminate()
        monitor_process.terminate()
        code_execution_process.join()
        monitor_process.join()


def code_function(
    test_case,
    allowed_memory_bytes=50,
    allowed_time_sec=10,
):
    result = execute(test_case, allowed_memory_bytes, allowed_time_sec)
    return json.loads(result)


def run_solution():
    results = []
    for test_case in [{'input': ['ABCABC', 'ABC'], 'output': 'ABC'}, {'input': ['ABABAB', 'ABAB'], 'output': 'AB'}, {'input': ['LEET', 'CODE'], 'output': ''}]:
        try:
            result = code_function(test_case, allowed_memory_bytes=100, allowed_time_sec=40)
            results.append(result)
        except Exception as e:
            raise Exception(e)
    
    return {"results": results}

if __name__ == "__main__":
    with open('/results/results.json', 'w') as dest:
        dest.write(json.dumps(run_solution()))