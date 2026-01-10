from datetime import datetime
from database.db import get_connection, init_db

init_db()

def log_ticket(message, intent, confidence, action):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_logs (timestamp, message, intent, confidence, action)
        VALUES (?, ?, ?, ?, ?)
    """, (
        str(datetime.now()),
        message,
        intent,
        confidence,
        action
    ))

    conn.commit()
    conn.close()
