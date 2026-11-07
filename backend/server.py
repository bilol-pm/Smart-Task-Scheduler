import sqlite3
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel

DB_PATH = Path(__file__).parent / "tasks.db"
app = FastAPI()

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks ORDER BY priority ").fetchall()
    conn.close()
    return [dict(row) for row in rows]

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: int


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)",
        (task.title, task.description, task.priority)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, "title": task.title}