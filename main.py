import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic import BaseModel, field_validator
import tempfile
import os
import json
import docker
import logging
import shutil
import redis.connection
import uvicorn
import ast
import redis
import uuid
from fastapi.middleware.cors import CORSMiddleware

DB_NAME = "problems_v9.db"
PROBLEM_TABLE = "problems"
MODULES_TABLE = "modules"
SUBMISSION_TEST_CASE_TABLE = "submission_test_cases"
LANG_TABLE = "langs"

redis_client = redis.Redis(host="localhost", port=6379, db=0)


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
            f"SELECT * FROM {PROBLEM_TABLE} WHERE questionId = ?", (problem_id,)
        ).fetchone()


def get_all_problems():
    with create_sql_connection() as _db:
        return _db.cursor.execute(f"SELECT * FROM {PROBLEM_TABLE}").fetchall()


def get_submission_test_cases(problem_id: str):
    with create_sql_connection() as _db:
        return _db.cursor.execute(
            f"SELECT * FROM {SUBMISSION_TEST_CASE_TABLE} WHERE questionId = ?",
            (problem_id,),
        ).fetchall()


def get_modules():
    with create_sql_connection() as _db:
        return _db.cursor.execute(f"SELECT * FROM {MODULES_TABLE}").fetchall()


def get_module(id: str):
    with create_sql_connection() as _db:
        return _db.cursor.execute(
            f"SELECT * FROM {MODULES_TABLE} WHERE id = ?", (id,)
        ).fetchone()


def get_problem_lang_options(problem_id: str):
    with create_sql_connection() as _db:
        return _db.cursor.execute(
            f"SELECT lang, label FROM {LANG_TABLE} WHERE questionId = ?", (problem_id,)
        ).fetchall()


def get_problem_lang_meta(lang: str, problem_id: str):
    with create_sql_connection() as _db:
        return _db.cursor.execute(
            f"SELECT * FROM {LANG_TABLE} WHERE questionId = ? AND lang = ?",
            (problem_id, lang),
        ).fetchone()


def admin_update_problem(problem_id: str, problem_update):
    with create_sql_connection() as _db:
        try:
            _db.cursor.execute(
                f"""
                UPDATE {PROBLEM_TABLE}
                SET title = ?, content = ?, initial_code = ?, validation_func = ?, test_cases = ?
                WHERE questionId = ?
                """,
                (
                    problem_update.title,
                    problem_update.content,
                    problem_update.initial_code,
                    problem_update.validation_func,
                    problem_update.test_cases,
                    problem_id,
                ),
            )
            _db.conn.commit()
        except sqlite3.Error as _:
            raise HTTPException(status_code=500, detail="invalid update data")


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
docker_client = docker.from_env()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/problem_page/{problem_id}", response_class=HTMLResponse)
async def problem_page(request: Request):
    return templates.TemplateResponse("problem.html", {"request": request})


class ProblemUpdate(BaseModel):
    title: str
    content: str
    initial_code: str
    validation_func: str
    test_cases: str

    @field_validator("initial_code")
    @classmethod
    def validate_initial_code(cls, v):
        try:
            tree = ast.parse(v)
            classes = [
                node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
            ]
            if not any(node.name == "Solution" for node in classes):
                raise ValueError("initial code must contain 'Solution' class")
            solution_class = [node for node in classes if node.name == "Solution"][0]
            solution_methods = [
                node
                for node in solution_class.body
                if isinstance(node, ast.FunctionDef)
            ]
            if len(solution_methods) == 0:
                raise ValueError(
                    "initial code Solution class must contain atleast one method for the execution"
                )
        except SyntaxError:
            raise ValueError("invalid python syntax in initial code")
        return v

    @field_validator("validation_func")
    @classmethod
    def validate_validation_func(cls, v):
        try:
            tree = ast.parse(v)
            classes = [
                node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
            ]
            if not any(node.name == "Validation" for node in classes):
                raise ValueError(
                    "validation function must contain a 'Validation' class"
                )
            validation_class = [node for node in classes if node.name == "Validation"][
                0
            ]
            methods = [
                node
                for node in validation_class.body
                if isinstance(node, ast.FunctionDef)
            ]
            if not any(method.name == "main" for method in methods):
                raise ValueError(
                    "validation code Validation class must contain a 'main' method"
                )
            main_method = [method for method in methods if method.name == "main"][0]
            main_method_returns = [
                node for node in ast.walk(main_method) if isinstance(node, ast.Return)
            ]
            if not main_method_returns or not isinstance(
                main_method_returns[0].value, ast.Tuple
            ):
                raise ValueError(
                    "validation function main method should return a tuple"
                )
        except SyntaxError:
            raise ValueError("invalid python syntax in validation code")
        return v

    @field_validator("test_cases")
    @classmethod
    def validate_test_cases(cls, v):
        try:
            cases = json.loads(v)
            if isinstance(cases, dict):
                cases = [cases]
            if isinstance(cases, list) and len(cases) == 0:
                raise ValueError(
                    "test cases can't be empty atleast include single test case"
                )
            for case in cases:
                if (
                    not isinstance(case, dict)
                    or "input_args" not in case
                    or "expected_return" not in case
                    or "input_kwargs" not in case
                ):
                    raise ValueError(
                        "each test case must be dict and each should have input_args, input_kwargs, expected_return return keys"
                    )
        except json.JSONDecodeError:
            raise ValueError("invalid json in test cases")
        return v


@app.put("/admin/update-problem/{problem_id}")
async def update_problem_route(problem_id: str, problem_update: ProblemUpdate):
    admin_update_problem(problem_id, problem_update)
    return {"message": "problem updated successfully"}


@app.get("/admin/edit-problem/{problem_id}", response_class=HTMLResponse)
async def admin_edit_problem_route(request: Request):
    return templates.TemplateResponse("edit_problem.html", {"request": request})


@app.get("/get_problem/{problem_id}")
async def get_problem_route(problem_id: str):
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="invalid problem id")
    return dict(problem)


@app.get("/all_problems")
async def get_all_problems_route():
    return {"problems": get_all_problems()}


def get_job_status(job_id: str):
    status_data = redis_client.get(f"jobs:{job_id}")
    return json.loads(status_data)


def set_job_status(job_id: str, status: str):
    redis_client.set(
        f"jobs:{job_id}", json.dumps({"status": "pending", "result": None})
    )


def create_job_id():
    return f"job_{uuid.uuid4()}"


def create_job(problem_id, code, job_type):
    job_id = create_job_id()
    run_code_input = {"problem_id": problem_id, "code": code}
    redis_client.rpush(
        "code_execution_queue",
        json.dumps(
            {"run_code_input": run_code_input, "job_id": job_id, "job_type": job_type}
        ),
    )
    set_job_status(job_id, status="pending")
    return job_id


class RunCodeInput(BaseModel):
    problem_id: str
    code: str


class SubmissionCodeInput(BaseModel):
    problem_id: str
    code: str


class CheckStatusInput(BaseModel):
    job_id: str


class GetModuleInput(BaseModel):
    module_id: str


@app.post("/check/status")
async def check_status(status_input: CheckStatusInput):
    job_id = status_input.job_id
    status_data = get_job_status(job_id) or {}
    return {
        "job_id": job_id,
        "status": status_data.get("status"),
        "result": status_data.get("result"),
    }


@app.get("/modules")
async def get_modules_route():
    return get_modules() or []


@app.get("/available_langs/{problem_id}")
def get_problem_lang_options_route(problem_id: str):
    return get_problem_lang_options(problem_id) or []


@app.get("/available_langs/{lang}/{problem_id}")
def get_problem_lang_meta_route(lang: str, problem_id: str):
    return get_problem_lang_meta(lang, problem_id) or {}


@app.post("/get-module")
async def get_module_route(input: GetModuleInput):
    module_id = input.module_id
    return get_module(module_id)


@app.post("/submit_code")
async def submit_code(submission_input: SubmissionCodeInput):
    problem_id, code = submission_input.problem_id, submission_input.code
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="invalid problem id")
    job_id = create_job(problem_id, code, job_type="submit")
    return {"job_id": job_id, "status": "pending", "result": None}


@app.post("/run_code")
async def run_code(run_code_input: RunCodeInput):
    problem_id, code = run_code_input.problem_id, run_code_input.code
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="invalid problem id")
    job_id = create_job(problem_id, code, job_type="run")
    return {"job_id": job_id, "status": "pending", "result": None}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
