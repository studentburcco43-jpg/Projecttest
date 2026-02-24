import sqlite3
from . import schemas
# CRUD = Create, Read, Update, Delete operations for managing database data
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