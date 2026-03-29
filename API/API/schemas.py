from pydantic import BaseModel

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
