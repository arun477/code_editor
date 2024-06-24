import sqlite3
from contextlib import contextmanager

DATABASE_NAME = "problems.db"

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            initial_code TEXT NOT NULL,
            test_case TEXT NOT NULL
        )
        ''')
        conn.commit()

def insert_problem(title, description, initial_code, test_case):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO problems (title, description, initial_code, test_case)
        VALUES (?, ?, ?, ?)
        ''', (title, description, initial_code, test_case))
        conn.commit()
        return cursor.lastrowid

def get_problem(problem_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM problems WHERE id = ?', (problem_id,))
        return cursor.fetchone()

def problem_exists(problem_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM problems WHERE id = ?', (problem_id,))
        return cursor.fetchone() is not None

def get_all_problem_ids():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM problems')
        return [row['id'] for row in cursor.fetchall()]

# Initialize the database and insert a sample problem
def setup_sample_problem():
    init_db()
    
    title = "Move Zeroes"
    description = """Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.

Note that you must do this in-place without making a copy of the array."""

    initial_code = """class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        \"\"\"
        Do not return anything, modify nums in-place instead.
        \"\"\"
        pass"""

    test_case = """
def test_solution(solution):
    # Test case 1
    nums1 = [0,1,0,3,12]
    solution.moveZeroes(nums1)
    assert nums1 == [1,3,12,0,0], f"Test case 1 failed. Expected [1,3,12,0,0], but got {nums1}"

    # Test case 2
    nums2 = [0]
    solution.moveZeroes(nums2)
    assert nums2 == [0], f"Test case 2 failed. Expected [0], but got {nums2}"

    print("All test cases passed!")

# Run the test
test_solution(Solution())
"""

    return insert_problem(title, description, initial_code, test_case)

if __name__ == "__main__":
    setup_sample_problem()