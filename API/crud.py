import sqlite3
from datetime import datetime, timezone
from . import schemas
# CRUD = Create, Read, Update, Delete operations for managing database data

# -----------------------------
# CRUD for User Table
# -----------------------------

def get_user_by_username(conn: sqlite3.Connection, username: str) -> "schemas.UserInDB | None":
    cur = conn.execute(
        "SELECT id, username, hashed_password, FirstName, LastName, LastLoginDate FROM user WHERE username = ?",
        (username,)
    )
    row = cur.fetchone()
    if row is None:
        return None
    return schemas.UserInDB(
        id=row["id"],
        username=row["username"],
        hashed_password=row["hashed_password"],
        FirstName=row["FirstName"],
        LastName=row["LastName"],
        LastLoginDate=row["LastLoginDate"],
    )

def create_user(conn: sqlite3.Connection, username: str, hashed_password: str, first_name: str, last_name: str) -> schemas.User:
    cur = conn.execute(
        "INSERT INTO user (username, hashed_password, FirstName, LastName) VALUES (?, ?, ?, ?);",
        (username, hashed_password, first_name, last_name)
    )
    conn.commit()
    return schemas.User(id=cur.lastrowid, username=username, FirstName=first_name, LastName=last_name)

def update_last_login(conn: sqlite3.Connection, user_id: int) -> None:
    conn.execute(
        "UPDATE user SET LastLoginDate = ? WHERE id = ?",
        (datetime.now(timezone.utc).isoformat(), user_id)
    )
    conn.commit()

# These functions handle all interactions with the service table

# READ - fetch all services from the database
def get_services(conn: sqlite3.Connection) -> list[schemas.Service]:
    cur = conn.execute("SELECT id, ServiceName, Cost FROM service ORDER BY id;")
    rows = cur.fetchall()
    return [schemas.Service(id=row["id"], ServiceName=row["ServiceName"], Cost=row["Cost"]) for row in rows]

# CREATE - insert a new service into the database
def create_service(conn: sqlite3.Connection, service: schemas.ServiceCreate) -> schemas.Service:
    cur = conn.execute(
        "INSERT INTO service (ServiceName, Cost) VALUES (?, ?);",
        (service.ServiceName, service.Cost)
    )
    conn.commit()

    new_id = cur.lastrowid
    return schemas.Service(id=new_id, ServiceName=service.ServiceName, Cost=service.Cost)

# DELETE - remove a service from the database by ID
def delete_service(conn: sqlite3.Connection, service_id: int) -> None:
    conn.execute("DELETE FROM service WHERE id = ?;", (service_id,))
    conn.commit()

# -----------------------------
# CRUD for Profit Table
# -----------------------------

def get_profits(conn: sqlite3.Connection) -> list[schemas.Profit]:
    cur = conn.execute(
        "SELECT id, category, revenue, expenses, notes FROM profit ORDER BY id;"
    )
    rows = cur.fetchall()
    return [
        schemas.Profit(
            id=row["id"],
            category=row["category"],
            revenue=row["revenue"],
            expenses=row["expenses"],
            notes=row["notes"]
        )
        for row in rows
    ]


def create_profit(conn: sqlite3.Connection, profit: schemas.ProfitCreate) -> schemas.Profit:
    cur = conn.execute(
        "INSERT INTO profit (category, revenue, expenses, notes) VALUES (?, ?, ?, ?);",
        (profit.category, profit.revenue, profit.expenses, profit.notes)
    )
    conn.commit()

    new_id = cur.lastrowid
    return schemas.Profit(
        id=new_id,
        category=profit.category,
        revenue=profit.revenue,
        expenses=profit.expenses,
        notes=profit.notes
    )


def delete_profit(conn: sqlite3.Connection, profit_id: int) -> None:
    conn.execute("DELETE FROM profit WHERE id = ?;", (profit_id,))
    conn.commit()


def get_profit(conn, profit_id: int):
    cur = conn.cursor()
    cur.execute(
        "SELECT id, category, revenue, expenses, notes FROM profit WHERE id = ?",
        (profit_id,)
    )
    row = cur.fetchone()

    if row:
        return schemas.Profit(
            id=row[0],
            category=row[1],
            revenue=row[2],
            expenses=row[3],
            notes=row[4]
        )
    return None


def update_profit(conn, profit_id: int, updates):
    cur = conn.cursor()
    cur.execute(
        "UPDATE profit SET category = ?, revenue = ?, expenses = ?, notes = ? WHERE id = ?",
        (updates.category, updates.revenue, updates.expenses, updates.notes, profit_id)
    )
    conn.commit()

    return get_profit(conn, profit_id)

# -----------------------------
# CRUD for Ad Table
# -----------------------------

def get_ads(conn: sqlite3.Connection) -> list[schemas.Ad]:
    cur = conn.execute(
        "SELECT id, campaign, impressions, clicks, cost, conversions, notes FROM ad ORDER BY id;"
    )
    rows = cur.fetchall()
    return [
        schemas.Ad(
            id=row["id"],
            campaign=row["campaign"],
            impressions=row["impressions"],
            clicks=row["clicks"],
            cost=row["cost"],
            conversions=row["conversions"],
            notes=row["notes"]
        )
        for row in rows
    ]


def create_ad(conn: sqlite3.Connection, ad: schemas.AdCreate) -> schemas.Ad:
    cur = conn.execute(
        "INSERT INTO ad (campaign, impressions, clicks, cost, conversions, notes) VALUES (?, ?, ?, ?, ?, ?);",
        (ad.campaign, ad.impressions, ad.clicks, ad.cost, ad.conversions, ad.notes)
    )
    conn.commit()

    new_id = cur.lastrowid
    return schemas.Ad(
        id=new_id,
        campaign=ad.campaign,
        impressions=ad.impressions,
        clicks=ad.clicks,
        cost=ad.cost,
        conversions=ad.conversions,
        notes=ad.notes
    )


def delete_ad(conn: sqlite3.Connection, ad_id: int) -> None:
    conn.execute("DELETE FROM ad WHERE id = ?;", (ad_id,))
    conn.commit()


def get_ad(conn, ad_id: int):
    cur = conn.cursor()
    cur.execute(
        "SELECT id, campaign, impressions, clicks, cost, conversions, notes FROM ad WHERE id = ?",
        (ad_id,)
    )
    row = cur.fetchone()

    if row:
        return schemas.Ad(
            id=row[0],
            campaign=row[1],
            impressions=row[2],
            clicks=row[3],
            cost=row[4],
            conversions=row[5],
            notes=row[6]
        )
    return None


def update_ad(conn, ad_id: int, updates):
    cur = conn.cursor()
    cur.execute(
        "UPDATE ad SET campaign = ?, impressions = ?, clicks = ?, cost = ?, conversions = ?, notes = ? WHERE id = ?",
        (updates.campaign, updates.impressions, updates.clicks, updates.cost, updates.conversions, updates.notes, ad_id)
    )
    conn.commit()

    return get_ad(conn, ad_id)

# -----------------------------
# CRUD for Client Table
# -----------------------------

def get_clients(conn: sqlite3.Connection) -> list[schemas.Client]:
    cur = conn.execute("SELECT id, ClientName FROM client ORDER BY id;")
    rows = cur.fetchall()
    return [schemas.Client(id=row["id"], ClientName=row["ClientName"]) for row in rows]

def create_client(conn: sqlite3.Connection, client: schemas.ClientCreate) -> schemas.Client:
    cur = conn.execute(
        "INSERT INTO client (ClientName) VALUES (?);",
        (client.ClientName,)
    )
    conn.commit()

    new_id = cur.lastrowid
    return schemas.Client(id=new_id, ClientName=client.ClientName)

def delete_client(conn: sqlite3.Connection, client_id: int) -> None:
    conn.execute("DELETE FROM client WHERE id = ?;", (client_id,))
    conn.commit()

# -----------------------------
# CRUD for Job Table
# -----------------------------

def get_jobs(conn: sqlite3.Connection) -> list[schemas.Job]:
    cur = conn.execute("""
        SELECT id, client_id, job_date, service_id, service_details, income, expenses, expense_notes, status 
        FROM job ORDER BY id;
    """)
    rows = cur.fetchall()
    return [
        schemas.Job(
            id=row["id"],
            client_id=row["client_id"],
            job_date=row["job_date"],
            service_id=row["service_id"],
            service_details=row["service_details"],
            income=row["income"],
            expenses=row["expenses"],
            expense_notes=row["expense_notes"],
            status=row["status"]
        )
        for row in rows
    ]

def create_job(conn: sqlite3.Connection, job: schemas.JobCreate) -> schemas.Job:
    cur = conn.execute(
        "INSERT INTO job (client_id, job_date, service_id, service_details, income, expenses, expense_notes, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
        (job.client_id, job.job_date, job.service_id, job.service_details, job.income, job.expenses, job.expense_notes, job.status)
    )
    conn.commit()

    new_id = cur.lastrowid
    return schemas.Job(
        id=new_id,
        client_id=job.client_id,
        job_date=job.job_date,
        service_id=job.service_id,
        service_details=job.service_details,
        income=job.income,
        expenses=job.expenses,
        expense_notes=job.expense_notes,
        status=job.status
    )

def delete_job(conn: sqlite3.Connection, job_id: int) -> None:
    conn.execute("DELETE FROM job WHERE id = ?;", (job_id,))
    conn.commit()

def get_job(conn, job_id: int):
    cur = conn.cursor()
    cur.execute(
        "SELECT id, client_id, job_date, service_id, service_details, income, expenses, expense_notes, status FROM job WHERE id = ?",
        (job_id,)
    )
    row = cur.fetchone()

    if row:
        return schemas.Job(
            id=row[0],
            client_id=row[1],
            job_date=row[2],
            service_id=row[3],
            service_details=row[4],
            income=row[5],
            expenses=row[6],
            expense_notes=row[7],
            status=row[8]
        )
    return None