import redis
import json
import docker
import time

class CodeExecutionWorker:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.docker_client = docker.from_env()

    def run_code(self, code):
        try:
            container = self.docker_client.containers.run(
                "python:3.9-slim",
                f"python -c \"{code}\"",
                detach=True,
                mem_limit="250m",
                cpu_quota=50000,
                network_mode="none"
            )
            output = container.logs().decode().strip()
            exit_code = container.wait()['StatusCode']
            container.remove()

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

def main():
    worker = CodeExecutionWorker()
    print("Worker started. Waiting for jobs...")
    worker.process_jobs()

if __name__ == "__main__":
    main()