from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    host = "http://localhost:8000"  # Replace with your application's base URL
    # wait_time = between(1, 2)

    @task(1)
    def get_problem(self):
        self.client.get("/get_problem/1894")

    # @task(1)
    # def run_code(self):
    #     code = """class Solution:
    # def mergeAlternately(self, word1, word2):
    #     merged = []
    #     i, j = 0, 0
        
    #     while i < len(word1) and j < len(word2):
    #         merged.append(word1[i])
    #         merged.append(word2[j])
    #         i += 1
    #         j += 1
        
    #     # Append remaining characters from word1 if any
    #     merged.extend(word1[i:])
    #     # Append remaining characters from word2 if any
    #     merged.extend(word2[j:])
        
    #     return ''.join(merged)"""
    #     self.client.post("/run_code", json={"problem_id": "1894", "code": code})

# if __name__ == "__main__":
#     import os
#     os.system("locust -f locustfile.py")