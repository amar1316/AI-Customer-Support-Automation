import sqlite3
from pathlib import Path

DB_PATH = Path("database.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            message TEXT,
            intent TEXT,
            confidence INTEGER,
            action TEXT
        )
    """)

    conn.commit()
    conn.close()
