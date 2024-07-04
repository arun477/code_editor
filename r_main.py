import sqlite3
from contextlib import contextmanager

DB_NAME = 'problems_v9.db'
PROBLEM_TABLE = 'problems'
SUBMISSION_TEST_CASE_TABLE = 'submission_test_cases'

@contextmanager
def create_sql_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        if conn:
            conn.close()