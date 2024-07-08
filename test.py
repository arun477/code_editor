import redis
import uuid
import json
import time

class CodeExecutionClient:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

    def submit_code(self, code, problem):
        job_id = str(uuid.uuid4())
        job_data = {
            'job_id': job_id,
            'code': code,
            'problem': problem,
            'status': 'pending'
        }
        # Create initial job entry
        self.redis_client.set(f"job:{job_id}", json.dumps(job_data))
        # Add job to queue
        self.redis_client.rpush('job_queue', json.dumps(job_data))
        print(f"Job {job_id} submitted and initial entry created")
        return job_id

    def get_job_status(self, job_id):
        job_data = self.redis_client.get(f"job:{job_id}")
        if job_data:
            try:
                job_info = json.loads(job_data)
                return job_info.get('status', 'unknown')
            except json.JSONDecodeError:
                return 'error'
        return 'not_found'

    def get_job_result(self, job_id):
        job_data = self.redis_client.get(f"job:{job_id}")
        if job_data:
            try:
                return json.loads(job_data)
            except json.JSONDecodeError:
                return {'status': 'error', 'message': 'Invalid job data'}
        return None

def main():
    client = CodeExecutionClient()

    code = 'print("Hello, World!")'
    problem = {'test_cases': [{'input': [], 'expected_output': 'Hello, World!'}]}

    job_id = client.submit_code(code, problem)
    print(f"Submitted job: {job_id}")

    max_attempts = 60  # Increased timeout
    attempt = 0
    while attempt < max_attempts:
        status = client.get_job_status(job_id)
        print(f"Job status: {status}")
        if status in ['completed', 'failed']:
            break
        time.sleep(1)
        attempt += 1

    if attempt == max_attempts:
        print("Job timed out")
    else:
        result = client.get_job_result(job_id)
        print(f"Job result: {result}")

if __name__ == "__main__":
    main()