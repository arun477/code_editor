import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import docker
import logging

DB_NAME = 'problems_v9.db'
PROBLEM_TABLE = 'problems'
SUBMISSION_TEST_CASE_TABLE = 'submission_test_cases'

class DB:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

@contextmanager
def create_sql_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        yield DB(cursor=conn.cursor(), conn=conn)
    finally:
        if conn:
            conn.close()

def get_problem(problem_id: str):
    with create_sql_connection() as _db:
        return _db.cursor.execute(
            f"SELECT * FROM {PROBLEM_TABLE} WHERE questionId = ?", (problem_id, )
        ).fetchone()  

def get_all_problems():
    with create_sql_connection() as _db:
        return _db.cursor.execute(
            f"SELECT * FROM {PROBLEM_TABLE}"
        ).fetchall()

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/assets', StaticFiles(directory='assets'), name='assets')
docker_client = docker.from_env()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


