import sqlite3
from contextlib import contextmanager

DB_PATH = "data.db"

def init_db() -> None:
    """Initialize the database schema if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    try:
        """Create the service table. Update this function to modify the schema as needed. And to add additional tables."""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS service (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                ServiceName  TEXT NOT NULL,
                Cost REAL NOT NULL
            )
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
