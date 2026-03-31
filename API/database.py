import sqlite3
from contextlib import contextmanager

DB_PATH = "data.db"

# Initialize database and create tables on startup
def init_db() -> None:
    """Initialize the database schema if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    try:
        # Create the service table to store service information
        conn.execute("""
            CREATE TABLE IF NOT EXISTS service (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                ServiceName  TEXT NOT NULL,
                Cost REAL NOT NULL
            );
        """)

        conn.execute("""
           CREATE TABLE IF NOT EXISTS profit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                revenue REAL NOT NULL,
                expenses REAL NOT NULL,
                notes TEXT
            );
        """)
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


# Context manager to safely get and close database connections
@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
