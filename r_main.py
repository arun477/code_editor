import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import docker
import logging
from pydantic import BaseModel

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

@app.get('/', response_class=HTMLResponse)
async def root(request:Request):
    return templates.TemplateResponse("index.html", {'request': request})

@app.get("/problem_page/{problem_id}", response_class=HTMLResponse)
async def problem_page(request:Request):
    return templates.TemplateResponse('problem.html', {'request': request})

@app.get("/problem/{problem_id}")
async def problem(problem_id: str):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail='invalid problem id')
    return dict(problem)

class RunCodeInput(BaseModel):
    problem_id: str
    code: str

@app.post("/run_code")
async def run_code(run_code_input:RunCodeInput):
    problem_id, code = run_code_input.problem_id, run_code_input.code
    result = run_in_docker(code, problem_id)
    return result or {}

