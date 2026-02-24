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

# You can add additional schemas for other tables here as needed by following the same pattern above