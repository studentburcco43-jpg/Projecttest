import sqlite3
from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db, get_conn
from . import crud, schemas
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


# ---- API Routes for Services ----
# API Route: GET all services - fetch all services from the database
@app.get("/api/services", response_model=list[schemas.Service])
def get_services(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_services(db)

# API Route: POST new service - create a new service in the database
@app.post("/api/services", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_service(db, service)

# API Route: DELETE a service - delete a service from the database by ID
@app.delete("/api/services/{service_id}", status_code=204)
def delete_service(service_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_service(db, service_id)
    return None

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

# ---- API Routes for Ad Reports ----

@app.get("/api/ads", response_model=list[schemas.Ad])
def get_ads(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_ads(db)

@app.post("/api/ads", response_model=schemas.Ad)
def create_ad(ad: schemas.AdCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_ad(db, ad)

@app.delete("/api/ads/{ad_id}", status_code=204)
def delete_ad(ad_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_ad(db, ad_id)
    return None

@app.get("/api/ads/{ad_id}", response_model=schemas.Ad)
def get_ad(ad_id: int, db: sqlite3.Connection = Depends(get_db)):
    ad = crud.get_ad(db, ad_id)
    if ad is None:
        return {"detail": "Not Found"}
    return ad

@app.put("/api/ads/{ad_id}", response_model=schemas.Ad)
def update_ad(ad_id: int, updates: schemas.AdCreate, db: sqlite3.Connection = Depends(get_db)):
    updated = crud.update_ad(db, ad_id, updates)
    if updated is None:
        return {"detail": "Not Found"}
    return updated

# ---- API Routes for Clients ----

@app.get("/api/clients", response_model=list[schemas.Client])
def get_clients(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_clients(db)

@app.post("/api/clients", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_client(db, client)

@app.delete("/api/clients/{client_id}", status_code=204)
def delete_client(client_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_client(db, client_id)
    return None

# ---- API Routes for Jobs ----

@app.get("/api/jobs", response_model=list[schemas.Job])
def get_jobs(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_jobs(db)

@app.post("/api/jobs", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_job(db, job)

@app.delete("/api/jobs/{job_id}", status_code=204)
def delete_job(job_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_job(db, job_id)
    return None

@app.get("/api/jobs/{job_id}", response_model=schemas.Job)
def get_job(job_id: int, db: sqlite3.Connection = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if job is None:
        return {"detail": "Not Found"}
    return job

# Mount the Web folder to serve HTML, CSS, and JS files - "/" automatically serves index.html
# Resolve an absolute path for the `Web` static folder so the app works
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "Web"
if not STATIC_DIR.exists():
    logging.warning("Static directory %s does not exist", STATIC_DIR)

app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="web")


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
