import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")
conn.commit()


def add_user(user_id: int):
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()


def count_users() -> int:
    cur.execute("SELECT COUNT(*) FROM users")
    return cur.fetchone()[0]
  
