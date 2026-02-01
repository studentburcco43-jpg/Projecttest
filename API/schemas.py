from pydantic import BaseModel

# Schema for Service table
class ServiceBase(BaseModel):
    ServiceName: str
    Cost: float

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int
#End Service table schema

# You can add additional schemas for other tables here as needed. Duplicate the pattern above.