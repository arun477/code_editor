import time
def simple_task(x, y):
    print('----------*---------')
    print(f"starting task: add {x} + {y}")
    time.sleep(10)
    result = x + y
    print(f"task completed {x} + {y} = {result}")
    print('----------*---------')
    return result