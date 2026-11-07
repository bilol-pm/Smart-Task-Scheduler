import sqlite3

conn = sqlite3.connect("tasks.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority INTEGER NOT NULL,
    done INTEGER NOT NULL DEFAULT 0
)
""")

cur.execute(
    "INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)",
    ("Write report", "Q3 numbers", 2),
)
cur.execute(
    "INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)",
    ("Call client", "Follow up with client", 1),
)

cur.execute("UPDATE tasks SET done = 1 WHERE id = ?", (2,))

cur.execute("DELETE FROM tasks WHERE id = ?", (1,))

conn.commit()

cur.execute("SELECT * FROM tasks ORDER BY priority")
print(cur.fetchall())
conn.close()