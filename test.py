import queue
import threading
import time
import random

order_queue = queue.Queue()

def place_order():
    orders = ['1', '2', '3', '4']
    while True:
        order = random.choice(orders)
        order_queue.put(order)
        print(f"order placed {order}")
        time.sleep(random.uniform(0.5, 2))

def process_order():
    while True:
        order = order_queue.get()
        print(f'processing order: {order}')
        time.sleep(random.uniform(1, 3))
        print(f'completed order: {order}')
        order_queue.task_done()

threading.Thread(target=place_order, daemon=True).start()
threading.Thread(target=process_order, daemon=True).start()

time.sleep(30)