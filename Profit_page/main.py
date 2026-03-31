import sqlite3
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from API.database import init_db, get_conn
from API import crud, schemas
from pathlib import Path
import logging

# Create the FastAPI application instance
app = FastAPI()

# Add CORS middleware - allows the frontend to communicate with the backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database tables when the app starts
init_db()

# Helper function that provides database connection to API routes
def get_db():
    with get_conn() as conn:
        yield conn

# ---- API Routes for Profit Tracker ----

@app.get("/api/profits", response_model=list[schemas.Profit])
def get_profits(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_profits(db)

@app.post("/api/profits", response_model=schemas.Profit)
def create_profit(profit: schemas.ProfitCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_profit(db, profit)

@app.delete("/api/profits/{profit_id}", status_code=204)
def delete_profit(profit_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_profit(db, profit_id)
    return None

# ---- STATIC FILES (Frontend) ----
# IMPORTANT: Mount static files *after* API routes and NOT at "/"
# We mount them at "/web" so they don't override /api/* routes.

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "web"

if not STATIC_DIR.exists():
    logging.warning("Static directory %s does not exist", STATIC_DIR)

# Serve frontend at /web instead of /
app.mount("/web", StaticFiles(directory=str(STATIC_DIR), html=True), name="web")

# Basic health-check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/profits/{profit_id}", response_model=schemas.Profit)
def get_profit(profit_id: int, db: sqlite3.Connection = Depends(get_db)):
    profit = crud.get_profit(db, profit_id)
    if profit is None:
        return {"detail": "Not Found"}
    return profit


@app.put("/api/profits/{profit_id}", response_model=schemas.Profit)
def update_profit(profit_id: int, updates: schemas.ProfitCreate, db: sqlite3.Connection = Depends(get_db)):
    updated = crud.update_profit(db, profit_id, updates)
    if updated is None:
        return {"detail": "Not Found"}
    return updated
