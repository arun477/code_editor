import redis
from rq import Worker, Queue, Connection

listen = ['default']
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
        