import sqlite3
from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db, get_conn
from . import crud, schemas

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

# Mount the Web folder to serve HTML, CSS, and JS files - "/" automatically serves index.html
app.mount("/", StaticFiles(directory="Web", html=True), name="web")
