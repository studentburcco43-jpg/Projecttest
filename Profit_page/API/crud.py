import sqlite3
from API import schemas

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
