import time
from rq import Queue
import redis
from test2 import simple_task


redis_conn = redis.Redis(host='localhost', port=6379, db=0)
q = Queue('default', connection=redis_conn)

for _ in range(2):
    job = q.enqueue(simple_task, 2, 3)
    print('job id', job.id)
    print('---------')

