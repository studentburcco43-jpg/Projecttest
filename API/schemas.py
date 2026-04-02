from pydantic import BaseModel

# Service Table Schema - defines the structure and validation for service data

class ServiceBase(BaseModel):
    # Base class with common service fields
    ServiceName: str
    Cost: float

class ServiceCreate(ServiceBase):
    # Schema used when creating a new service (no ID needed, it's auto-generated)
    pass

class Service(ServiceBase):
    # Schema used when returning a service from the database (includes ID)
    id: int

# -----------------------------
# Profit Table Schemas
# -----------------------------

class ProfitBase(BaseModel):
    category: str
    revenue: float
    expenses: float
    notes: str | None = None

class ProfitCreate(ProfitBase):
    pass

class Profit(ProfitBase):
    id: int

# -----------------------------
# Ad Table Schemas
# -----------------------------

class AdBase(BaseModel):
    campaign: str
    impressions: int
    clicks: int
    cost: float
    conversions: int | None = None
    notes: str | None = None

class AdCreate(AdBase):
    pass

class Ad(AdBase):
    id: int

# -----------------------------
# Client Table Schemas
# -----------------------------

class ClientBase(BaseModel):
    ClientName: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int

# -----------------------------
# Job Table Schemas
# -----------------------------

class JobBase(BaseModel):
    client_id: int
    job_date: str
    service_id: int
    service_details: str | None = None
    income: float
    expenses: float
    expense_notes: str | None = None
    status: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int

# You can add additional schemas for other tables here as needed by following the same pattern above
