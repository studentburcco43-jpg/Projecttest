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
        # Create the ad table to store ad report entries
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign TEXT NOT NULL,
                impressions INTEGER NOT NULL,
                clicks INTEGER NOT NULL,
                cost REAL NOT NULL,
                conversions INTEGER,
                notes TEXT
            );
        """)

        # Create the client table to store client information
        conn.execute("""
            CREATE TABLE IF NOT EXISTS client (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ClientName TEXT NOT NULL
            );
        """)

        # Create the job table to store job entries
        conn.execute("""
            CREATE TABLE IF NOT EXISTS job (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                job_date TEXT NOT NULL,
                service_id INTEGER NOT NULL,
                service_details TEXT,
                income REAL NOT NULL,
                expenses REAL NOT NULL,
                expense_notes TEXT,
                status TEXT NOT NULL,
                FOREIGN KEY (client_id) REFERENCES client (id),
                FOREIGN KEY (service_id) REFERENCES service (id)
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
