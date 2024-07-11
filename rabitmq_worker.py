import redis
import json
import docker
import time
from queue import Queue
from threading import Thread

class CodeExecutionWorker:
    def __init__(self, redis_host='localhost', redis_port=6379, pool_size=5):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.docker_client = docker.from_env()
        self.container_pool = Queue()
        self.pool_size = pool_size
        self._initialize_container_pool()

    def _initialize_container_pool(self):
        for _ in range(self.pool_size):
            container = self.docker_client.containers.run(
                "python:3.9-slim",
                "tail -f /dev/null",  # Keep container running
                detach=True,
                mem_limit="250m",
                cpu_quota=50000,
                network_mode="none"
            )
            self.container_pool.put(container)

    def _get_container(self):
        return self.container_pool.get()

    def _return_container(self, container):
        self.container_pool.put(container)

    def run_code(self, code):
        container = self._get_container()
        try:
            exec_result = container.exec_run(f"python -c \"{code}\"")
            output = exec_result.output.decode().strip()
            exit_code = exec_result.exit_code
            
            return {
                'output': output,
                'exit_code': exit_code,
                'status': 'completed'
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }
        finally:
            self._return_container(container)

    def process_jobs(self):
        while True:
            job = self.redis_client.blpop('job_queue', timeout=1)
            if job:
                job_data = json.loads(job[1])
                job_id = job_data['job_id']
                code = job_data['code']

                print(f"Processing job: {job_id}")
                result = self.run_code(code)
                
                # Update job data
                job_data.update({
                    'result': result,
                    'status': result['status']
                })
                self.redis_client.set(f"job:{job_id}", json.dumps(job_data))
                print(f"Job {job_id} completed with status: {result['status']}")
            else:
                print("No jobs in queue. Waiting...")
                time.sleep(1)

    def cleanup(self):
        while not self.container_pool.empty():
            container = self.container_pool.get()
            container.stop()
            container.remove()

def main():
    worker = CodeExecutionWorker()
    try:
        print("Worker started. Waiting for jobs...")
        worker.process_jobs()
    finally:
        worker.cleanup()

if __name__ == "__main__":
    main()