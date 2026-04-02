# This import brings in the sqlite3 module, which allows the program to interact with SQLite databases for storing and retrieving data.
import sqlite3

# This import brings in specific components from the FastAPI framework, including FastAPI for creating the web application, Depends for dependency injection, and Request for handling HTTP requests.
from fastapi import FastAPI, Depends, Request

# This import brings in StaticFiles from FastAPI, which is used to serve static files like HTML, CSS, and JavaScript files to the web browser.
from fastapi.staticfiles import StaticFiles

# This import brings in CORSMiddleware from FastAPI, which handles Cross-Origin Resource Sharing to allow the frontend to communicate with the backend.
from fastapi.middleware.cors import CORSMiddleware

# This import brings in functions from the local database module, including init_db to set up the database and get_conn to get a database connection.
from .database import init_db, get_conn

# This import brings in the crud and schemas modules from the current package, which contain functions for database operations and data models.
from . import crud, schemas

# This import brings in the Path class from pathlib, which is used for working with file and directory paths in a cross-platform way.
from pathlib import Path

# This import brings in the logging module, which is used to record messages about the program's operation for debugging and monitoring.
import logging

# This line creates a new instance of the FastAPI application, which is the main object that handles all the web requests and responses for the API.
app = FastAPI()

# This block adds Cross-Origin Resource Sharing (CORS) middleware to the FastAPI application. CORS allows the frontend website to make requests to the API even if they are hosted on different domains, which is necessary for web applications.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This setting allows requests from any origin, which is useful for development but should be restricted in production for security.
    allow_credentials=True,  # This allows cookies and authentication headers to be included in requests.
    allow_methods=["*"],  # This allows all HTTP methods like GET, POST, PUT, DELETE.
    allow_headers=["*"],  # This allows all headers in requests.
)

# This line calls the init_db function to initialize the database tables when the application starts, ensuring the database is ready for use.
init_db()

# This is a helper function that provides a database connection to the API routes. It uses a context manager to ensure the connection is properly opened and closed, preventing resource leaks.
def get_db():
    with get_conn() as conn:
        yield conn

# This section defines the API routes for managing services. Services are items that the business offers to customers.

# This defines an API endpoint that responds to GET requests at /api/services. It fetches all services from the database and returns them as a list.
@app.get("/api/services", response_model=list[schemas.Service])
def get_services(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_services(db)

# This defines an API endpoint that responds to POST requests at /api/services. It creates a new service in the database based on the data provided in the request.
@app.post("/api/services", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_service(db, service)

# This defines an API endpoint that responds to DELETE requests at /api/services/{service_id}. It deletes the service with the specified ID from the database.
@app.delete("/api/services/{service_id}", status_code=204)
def delete_service(service_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_service(db, service_id)
    return None

# This section defines the API routes for managing profit records. Profits track the financial earnings from jobs or services.

# This defines an API endpoint that responds to GET requests at /api/profits. It fetches all profit records from the database and returns them as a list.
@app.get("/api/profits", response_model=list[schemas.Profit])
def get_profits(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_profits(db)

# This defines an API endpoint that responds to POST requests at /api/profits. It creates a new profit record in the database based on the data provided in the request.
@app.post("/api/profits", response_model=schemas.Profit)
def create_profit(profit: schemas.ProfitCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_profit(db, profit)

# This defines an API endpoint that responds to DELETE requests at /api/profits/{profit_id}. It deletes the profit record with the specified ID from the database.
@app.delete("/api/profits/{profit_id}", status_code=204)
def delete_profit(profit_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_profit(db, profit_id)
    return None

# This defines an API endpoint that responds to GET requests at /api/profits/{profit_id}. It fetches a single profit record by its ID from the database.
@app.get("/api/profits/{profit_id}", response_model=schemas.Profit)
def get_profit(profit_id: int, db: sqlite3.Connection = Depends(get_db)):
    profit = crud.get_profit(db, profit_id)
    if profit is None:
        return {"detail": "Not Found"}
    return profit

# This defines an API endpoint that responds to PUT requests at /api/profits/{profit_id}. It updates an existing profit record with new data provided in the request.
@app.put("/api/profits/{profit_id}", response_model=schemas.Profit)
def update_profit(profit_id: int, updates: schemas.ProfitCreate, db: sqlite3.Connection = Depends(get_db)):
    updated = crud.update_profit(db, profit_id, updates)
    if updated is None:
        return {"detail": "Not Found"}
    return updated

# This section defines the API routes for managing ad reports. Ad reports track advertising campaigns and their performance.

# This defines an API endpoint that responds to GET requests at /api/ads. It fetches all ad reports from the database and returns them as a list.
@app.get("/api/ads", response_model=list[schemas.Ad])
def get_ads(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_ads(db)

# This defines an API endpoint that responds to POST requests at /api/ads. It creates a new ad report in the database based on the data provided in the request.
@app.post("/api/ads", response_model=schemas.Ad)
def create_ad(ad: schemas.AdCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_ad(db, ad)

# This defines an API endpoint that responds to DELETE requests at /api/ads/{ad_id}. It deletes the ad report with the specified ID from the database.
@app.delete("/api/ads/{ad_id}", status_code=204)
def delete_ad(ad_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_ad(db, ad_id)
    return None

# This defines an API endpoint that responds to GET requests at /api/ads/{ad_id}. It fetches a single ad report by its ID from the database.
@app.get("/api/ads/{ad_id}", response_model=schemas.Ad)
def get_ad(ad_id: int, db: sqlite3.Connection = Depends(get_db)):
    ad = crud.get_ad(db, ad_id)
    if ad is None:
        return {"detail": "Not Found"}
    return ad

# This defines an API endpoint that responds to PUT requests at /api/ads/{ad_id}. It updates an existing ad report with new data provided in the request.
@app.put("/api/ads/{ad_id}", response_model=schemas.Ad)
def update_ad(ad_id: int, updates: schemas.AdCreate, db: sqlite3.Connection = Depends(get_db)):
    updated = crud.update_ad(db, ad_id, updates)
    if updated is None:
        return {"detail": "Not Found"}
    return updated

# This section defines the API routes for managing clients. Clients are the customers who hire the business for services.

# This defines an API endpoint that responds to GET requests at /api/clients. It fetches all clients from the database and returns them as a list.
@app.get("/api/clients", response_model=list[schemas.Client])
def get_clients(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_clients(db)

# This defines an API endpoint that responds to POST requests at /api/clients. It creates a new client record in the database based on the data provided in the request.
@app.post("/api/clients", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_client(db, client)

# This defines an API endpoint that responds to DELETE requests at /api/clients/{client_id}. It deletes the client record with the specified ID from the database.
@app.delete("/api/clients/{client_id}", status_code=204)
def delete_client(client_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_client(db, client_id)
    return None

# This section defines the API routes for managing jobs. Jobs are the specific tasks or projects assigned to clients.

# This defines an API endpoint that responds to GET requests at /api/jobs. It fetches all jobs from the database and returns them as a list.
@app.get("/api/jobs", response_model=list[schemas.Job])
def get_jobs(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_jobs(db)

# This defines an API endpoint that responds to POST requests at /api/jobs. It creates a new job record in the database based on the data provided in the request.
@app.post("/api/jobs", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_job(db, job)

# This defines an API endpoint that responds to DELETE requests at /api/jobs/{job_id}. It deletes the job record with the specified ID from the database.
@app.delete("/api/jobs/{job_id}", status_code=204)
def delete_job(job_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_job(db, job_id)
    return None

# This defines an API endpoint that responds to GET requests at /api/jobs/{job_id}. It fetches a single job record by its ID from the database.
@app.get("/api/jobs/{job_id}", response_model=schemas.Job)
def get_job(job_id: int, db: sqlite3.Connection = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if job is None:
        return {"detail": "Not Found"}
    return job

# This section sets up the serving of static files like HTML, CSS, and JavaScript for the web interface.

# This calculates the base directory of the project by finding the parent directory of the current file's directory.
BASE_DIR = Path(__file__).resolve().parent.parent

# This sets the path to the Web directory, which contains the static files for the website.
STATIC_DIR = BASE_DIR / "Web"

# This checks if the static directory exists, and logs a warning if it doesn't, to help with troubleshooting.
if not STATIC_DIR.exists():
    logging.warning("Static directory %s does not exist", STATIC_DIR)

# This mounts the static files directory to the root path "/", so that the web browser can access the HTML, CSS, and JS files. The html=True parameter allows serving index.html automatically.
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="web")

# This defines a basic health-check endpoint at /health, which returns a simple status message to confirm the API is running.
@app.get("/health")
def health():
    return {"status": "ok"}
