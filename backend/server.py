import sqlite3
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

DB_PATH = Path(__file__).parent / "tasks.db"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

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

class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    priority: int
    done: bool
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    conn = get_connection()
    cur = conn.execute(
        "UPDATE tasks SET title = ?, description = ?, priority = ?, done = ? WHERE id = ?",
        (task.title, task.description, task.priority, task.done, task_id),
    )
    conn.commit()
    updated = cur.rowcount
    conn.close()
    if updated == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return {"updated": task_id}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return {"deleted": task_id}

