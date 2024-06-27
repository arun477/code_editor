from typing import *
from string import *
from re import *
from datetime import *
from collections import *
from heapq import *
from bisect import *
from copy import *
from math import *
from random import *
from statistics import *
from itertools import *
from functools import *
from operator import *
from io import *
from sys import *
from json import *
from builtins import *

import resource
import time as time_moulde
import signal
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import json
import threading


class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        # while True:
        #     pass
        if str1 == 'ABABAB':
            sum([1]* 11 * 10**7)
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a

        if str1 + str2 != str2 + str1:
            return ""

        gcd_len = gcd(len(str1), len(str2))
        return str1[:gcd_len]


def set_resource_limits(mem_limit_mb, cpu_time_limit_sec):
    _, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (mem_limit_mb * 1024**2, hard))

    _, hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_time_limit_sec, hard))


def execute(args, kwargs, timeout, mem_limit_mb):
    start = time_moulde.time()
    return_output = None
    error = None
    std_logs = StringIO()
    std_err = StringIO()

    def check_memory_usage():
        current_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024  # ru_maxrss is in KB
        if current_memory >= (mem_limit_mb * 1024**2):
            raise MemoryError("Memory Limit Exceeded")

    def memory_limiting_handler(signum, frame):
        check_memory_usage()


    def handle_timeout(signum, frame):
        raise TimeoutError("Time Limit Exceeded")

    signal.signal(signal.SIGALRM, handle_timeout)
    signal.alarm(timeout)

    signal.signal(signal.SIGPROF, memory_limiting_handler)
    signal.setitimer(signal.ITIMER_PROF, 0.1, 0.1) 

    try:
        with redirect_stdout(std_logs), redirect_stderr(std_err):
            func = Solution().gcdOfStrings
            return_output = func(*args, **kwargs)
    except MemoryError as e:
        error = "Memory Limit Exceeded"
    except TimeoutError as e:
        error = "Time Limit Exceeded"
    except Exception as e:
        error = str(e)
    finally:
        signal.alarm(0)
        signal.setitimer(signal.ITIMER_PROF, 0, 0)

    end = time_moulde.time()
    time_took = end - start
    return {
        "return_output": return_output,
        "time_took": time_took,
        "error": error,
        "std_logs": std_logs.getvalue(),
        "std_err": error or std_err.getvalue(),
    }


def code_func(
    validation_func, test_case, allowed_time_sec, allowed_memory_mb
):
    input_args = test_case["input_args"]
    input_kwargs = test_case["input_kwargs"]
    expected_return = test_case["expected_return"]

    valid = False
    return_output = None
    error = None
    std_logs = None
    std_err = None

    set_resource_limits(allowed_memory_mb, allowed_time_sec)
    call_func_return = execute(input_args, input_kwargs, allowed_time_sec, allowed_memory_mb)
    std_logs = call_func_return["std_logs"]
    std_err = call_func_return['std_err']
    return_output = call_func_return["return_output"]
    error = call_func_return['error']

    if call_func_return["error"]:
        return {
            "input": str((input_args, input_kwargs)),
            "valid": valid,
            "error": error,
            "output": return_output,
            "std_logs": std_logs,
            "expected": expected_return,
            "std_err": error or std_err,
        }
    else:
        valid = validation_func(
            input_args, input_kwargs, expected_return, return_output
        )
        return {
            "input": str((input_args, input_kwargs)),
            "valid": valid,
            "error": error,
            "output": return_output,
            "std_logs": std_logs,
            "expected": expected_return,
            "std_err": std_err,
        }

def validation_func( input_args, input_kwargs, expected_return, return_output):
    valid = None
    valid = expected_return == return_output
    return valid

def run():
    with open("/app/test_cases.json", "r") as f:
        test_cases = json.loads(f.read())

    results = []
    for _, test_case in enumerate(test_cases):
        output = code_func(
            validation_func,
            test_case,
            allowed_time_sec=10,
            allowed_memory_mb=100,
        )
        results.append(output)
        if output["error"] == "Time Limit Exceeded" or output['error'] == 'Memory Limit Exceeded':
            break

    return {"results": results}


if __name__ == "__main__":
    try:
        output = run()
        with open("/app/results.json", "w") as dest:
            json.dump(output, dest)
    except Exception as e:
        print(e)