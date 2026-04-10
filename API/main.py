# This import brings in the sqlite3 module, which allows the program to interact with SQLite databases for storing and retrieving data.
import sqlite3

# This import brings in specific components from the FastAPI framework.
from fastapi import FastAPI, Depends, HTTPException, Request, Response, status, Cookie
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

# This import brings in StaticFiles from FastAPI, which is used to serve static files like HTML, CSS, and JavaScript files to the web browser.
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# This import brings in CORSMiddleware from FastAPI, which handles Cross-Origin Resource Sharing to allow the frontend to communicate with the backend.
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt

# This import brings in functions from the local database module.
from .database import init_db, get_db

# This import brings in the crud and schemas modules from the current package.
from . import crud, schemas

# This import brings in authentication utilities.
from .auth import (
    create_access_token,
    hash_password,
    verify_password,
    get_current_user,
    COOKIE_NAME,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM,
)

# This import brings in the Path class from pathlib.
from pathlib import Path

# This import brings in the logging module.
import logging

# This import brings in the os module for reading environment variables.
import os

# Read environment variables for HTTPS configuration.
# Set HTTPS=true when running behind TLS (uvicorn --ssl-certfile / --ssl-keyfile or a reverse proxy).
HTTPS_ENABLED: bool = os.environ.get("HTTPS", "false").lower() == "true"
# Set HTTPS_REDIRECT=true to automatically redirect all HTTP requests to HTTPS.
HTTPS_REDIRECT: bool = os.environ.get("HTTPS_REDIRECT", "false").lower() == "true"

# This line creates a new instance of the FastAPI application.
app = FastAPI()

# Redirect HTTP → HTTPS when HTTPS_REDIRECT is enabled (e.g. in production behind a load balancer).
if HTTPS_REDIRECT:
    from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
    app.add_middleware(HTTPSRedirectMiddleware)

# CORS middleware — should be restricted to specific origins in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This line initialises the database tables when the application starts.
init_db()

# ---------------------------------------------------------------------------
# Auth endpoints (public — no login required)
# ---------------------------------------------------------------------------

@app.post("/auth/register", response_model=schemas.User, tags=["auth"])
def register(user: schemas.UserCreate, db: sqlite3.Connection = Depends(get_db)):
    """Create a new user account."""
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = hash_password(user.password)
    return crud.create_user(db, user.username, hashed, user.FirstName, user.LastName)


@app.post("/auth/login", tags=["auth"])
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: sqlite3.Connection = Depends(get_db),
):
    """Authenticate with username and password; sets an HttpOnly session cookie on success."""
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    crud.update_last_login(db, user.id)
    token = create_access_token({"sub": user.username})
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=HTTPS_ENABLED,  # Automatically True when HTTPS=true env var is set
    )
    return {"message": "Login successful"}


@app.post("/auth/logout", tags=["auth"])
def logout(response: Response):
    """Clear the session cookie."""
    response.delete_cookie(COOKIE_NAME)
    return {"message": "Logged out"}


@app.get("/auth/me", response_model=schemas.User, tags=["auth"])
def get_me(current_user: schemas.User = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return current_user


# ---------------------------------------------------------------------------
# Protected API router — all routes require a valid session cookie
# ---------------------------------------------------------------------------

api_router = APIRouter(prefix="/api", dependencies=[Depends(get_current_user)])

# --- Services ---

@api_router.get("/services", response_model=list[schemas.Service])
def get_services(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_services(db)

@api_router.post("/services", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_service(db, service)

@api_router.delete("/services/{service_id}", status_code=204)
def delete_service(service_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_service(db, service_id)
    return None

# --- Profits ---

@api_router.get("/profits", response_model=list[schemas.Profit])
def get_profits(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_profits(db)

@api_router.post("/profits", response_model=schemas.Profit)
def create_profit(profit: schemas.ProfitCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_profit(db, profit)

@api_router.delete("/profits/{profit_id}", status_code=204)
def delete_profit(profit_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_profit(db, profit_id)
    return None

@api_router.get("/profits/{profit_id}", response_model=schemas.Profit)
def get_profit(profit_id: int, db: sqlite3.Connection = Depends(get_db)):
    profit = crud.get_profit(db, profit_id)
    if profit is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return profit

@api_router.put("/profits/{profit_id}", response_model=schemas.Profit)
def update_profit(profit_id: int, updates: schemas.ProfitCreate, db: sqlite3.Connection = Depends(get_db)):
    updated = crud.update_profit(db, profit_id, updates)
    if updated is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated

# --- Ads ---

@api_router.get("/ads", response_model=list[schemas.Ad])
def get_ads(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_ads(db)

@api_router.post("/ads", response_model=schemas.Ad)
def create_ad(ad: schemas.AdCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_ad(db, ad)

@api_router.delete("/ads/{ad_id}", status_code=204)
def delete_ad(ad_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_ad(db, ad_id)
    return None

@api_router.get("/ads/{ad_id}", response_model=schemas.Ad)
def get_ad(ad_id: int, db: sqlite3.Connection = Depends(get_db)):
    ad = crud.get_ad(db, ad_id)
    if ad is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return ad

@api_router.put("/ads/{ad_id}", response_model=schemas.Ad)
def update_ad(ad_id: int, updates: schemas.AdCreate, db: sqlite3.Connection = Depends(get_db)):
    updated = crud.update_ad(db, ad_id, updates)
    if updated is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated

# --- Clients ---

@api_router.get("/clients", response_model=list[schemas.Client])
def get_clients(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_clients(db)

@api_router.post("/clients", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_client(db, client)

@api_router.delete("/clients/{client_id}", status_code=204)
def delete_client(client_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_client(db, client_id)
    return None

# --- Jobs ---

@api_router.get("/jobs", response_model=list[schemas.Job])
def get_jobs(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_jobs(db)

@api_router.post("/jobs", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: sqlite3.Connection = Depends(get_db)):
    return crud.create_job(db, job)

@api_router.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int, db: sqlite3.Connection = Depends(get_db)):
    crud.delete_job(db, job_id)
    return None

@api_router.get("/jobs/{job_id}", response_model=schemas.Job)
def get_job(job_id: int, db: sqlite3.Connection = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return job

# --- Users ---
@api_router.get("/users", response_model=list[schemas.User])
def get_users(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_users(db)

@api_router.post("/users", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: sqlite3.Connection = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = hash_password(user.password)
    return crud.create_user(db, user.username, hashed, user.FirstName, user.LastName)

@api_router.put("/users/{user_id}", response_model=list[schemas.User])
def update_user(user_id: int, updates: schemas.UserUpdate, db: sqlite3.Connection = Depends(get_db)):
    hashed = hash_password(updates.password) if updates.password else None
    updated = crud.update_user(db, user_id, updates, hashed)
    if updated is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated

@api_router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    return crud.delete_user(db, user_id)

app.include_router(api_router)

# ---------------------------------------------------------------------------
# Static file serving and Jinja2 templates
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "Web"
TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", include_in_schema=False)
def index_page():
    return RedirectResponse(url="/index.html", status_code=302)


def _get_page_user(access_token: str | None = Cookie(default=None)) -> str | None:
    """Page-level auth check: returns the username or None (no exception raised)."""
    if not access_token:
        return None
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


@app.get("/quick-entry.html", include_in_schema=False)
def quick_entry_page(request: Request, username: str | None = Depends(_get_page_user)):
    if not username:
        return RedirectResponse(url="/login.html", status_code=302)
    return templates.TemplateResponse("quick-entry.html", {"request": request})


@app.get("/job.html", include_in_schema=False)
def job_page(request: Request, username: str | None = Depends(_get_page_user)):
    if not username:
        return RedirectResponse(url="/login.html", status_code=302)
    return templates.TemplateResponse("job.html", {"request": request})


@app.get("/profit.html", include_in_schema=False)
def profit_page(request: Request, username: str | None = Depends(_get_page_user)):
    if not username:
        return RedirectResponse(url="/login.html", status_code=302)
    return templates.TemplateResponse("profit.html", {"request": request})

@app.get("/admin.html", include_in_schema=False)
def admin_page(request: Request, username: str | None = Depends(_get_page_user)):
    if not username:
        return RedirectResponse(url="/login.html", status_code=302)
    return templates.TemplateResponse("admin.html", {"request": request})

if not STATIC_DIR.exists():
    logging.warning("Static directory %s does not exist", STATIC_DIR)

app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="web")

