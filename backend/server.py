import sqlite3
from pathlib import Path
from fastapi import FastAPI

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