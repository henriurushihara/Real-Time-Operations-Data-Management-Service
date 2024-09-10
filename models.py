from pydantic import BaseModel
from typing import Optional
from datetime import date

class Division(BaseModel):
    Division_Id: int
    Division_Name: str

class DivisionSummary(BaseModel):
    Division_Id: int
    Division_Name: str
    Well_Count: int
    Total_Oil_Produced: float
    Total_Budget: float
    Total_Actual: float
    Total_Oil_Sales: float

class WellSummary(BaseModel):
    well_id: int
    well_name: str
    division_id: int
    division_name: str
    total_oil_produced: float
    total_budget: float
    total_actual: float
    total_oil_sales: float

class WellSummaryByDay(BaseModel):
    well_id: int
    well_name: str
    division_id: int
    division_name: str
    date_value: date
    oil_produced: float
    oil_price: Optional[float]
    oil_sales: float
