import sqlite3
from contextlib import contextmanager

DB_PATH = "data.db"

def init_db() -> None:
    """Initialize the database schema if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    try:
        # Create the profit table to store profit tracker entries
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                revenue REAL NOT NULL,
                expenses REAL NOT NULL,
                notes TEXT
            );
        """)
        conn.commit()
    finally:
        conn.close()


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
