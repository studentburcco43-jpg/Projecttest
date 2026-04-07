# This import brings in the sqlite3 module, which allows the program to interact with SQLite databases for storing and retrieving data.
import sqlite3

# This import brings in the contextmanager decorator from the contextlib module, which is used to create a context manager for managing database connections safely.
from contextlib import contextmanager

# This variable defines the path to the SQLite database file where all data will be stored.
DB_PATH = "data.db"

# This function initializes the database and creates all necessary tables when the application starts up.
def init_db() -> None:
    """This docstring explains that the function initializes the database schema if it doesn't already exist."""
    # This line establishes a connection to the SQLite database file.
    conn = sqlite3.connect(DB_PATH)
    try:
        # This SQL command creates the service table to store information about the services offered by the business, including an ID, name, and cost.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS service (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                ServiceName  TEXT NOT NULL,
                Cost REAL NOT NULL
            );
        """)

        # This SQL command creates the profit table to store profit tracker entries, including category, revenue, expenses, and notes.
        conn.execute("""
           CREATE TABLE IF NOT EXISTS profit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                revenue REAL NOT NULL,
                expenses REAL NOT NULL,
                notes TEXT
            );
        """)
        # This SQL command creates the ad table to store ad report entries, including campaign details, impressions, clicks, cost, conversions, and notes.
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

        # This SQL command creates the client table to store client information, including an ID and client name.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS client (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ClientName TEXT NOT NULL
            );
        """)

        # This SQL command creates the user table to store user accounts with hashed credentials and profile info.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL,
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL,
                LastLoginDate TEXT
            );
        """)

        # This SQL command creates the job table to store job entries, including client ID, job date, service ID, details, income, expenses, notes, and status, with foreign keys to client and service tables.
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

        # This line commits all the changes to the database, making them permanent.
        conn.commit()


    finally:
        # This ensures the database connection is closed properly, even if an error occurs.
        conn.close()


# This generator function provides a database connection as a FastAPI dependency, used with Depends().
def get_db():
    with get_conn() as conn:
        yield conn


# This decorator defines a context manager to safely get and close database connections, preventing resource leaks.
@contextmanager
def get_conn():
    # This line creates a new connection to the database, with check_same_thread set to False to allow use in multi-threaded environments.
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    # This sets the row factory to sqlite3.Row, which allows accessing columns by name.
    conn.row_factory = sqlite3.Row
    try:
        # This yields the connection to the calling code, allowing it to be used.
        yield conn
    finally:
        # This ensures the connection is closed after use.
        conn.close()
