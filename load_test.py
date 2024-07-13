from locust import HttpUser, task, between
import time

class QuickstartUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 5)

    @task(1)
    def run_code(self):
        code = """class Solution:
    def mergeAlternately(self, word1, word2):
        merged = []
        i, j = 0, 0
        
        while i < len(word1) and j < len(word2):
            merged.append(word1[i])
            merged.append(word2[j])
            i += 1
            j += 1
        
        # Append remaining characters from word1 if any
        merged.extend(word1[i:])
        # Append remaining characters from word2 if any
        merged.extend(word2[j:])
        
        return ''.join(merged)"""
        
        response = self.client.post("/run_code", json={"problem_id": "1894", "code": code})
        if response.status_code == 200:
            job_id = response.json().get("job_id")
            if job_id:
                self.wait_for_completion(job_id)

    def wait_for_completion(self, job_id):
        max_attempts = 25
        delay = 0.3 # 1 second

        for attempt in range(max_attempts):
            response = self.client.post("/check/status", json={"job_id": job_id})
            if response.status_code == 200:
                status = response.json().get("status")
                if status == "done":
                    return
            time.sleep(delay)
