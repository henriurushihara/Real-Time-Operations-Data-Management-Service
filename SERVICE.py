from data_helper import DataHelper
from fastapi import FastAPI, Depends, HTTPException
from typing import List
import logging
import json
from models import Division, DivisionSummary, WellSummary, WellSummaryByDay  # Import the models

app = FastAPI()

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Dependency to get a DataHelper instance
def get_db():
    return DataHelper._instance

@app.on_event("startup")
async def on_startup():
    await DataHelper().initialize()

@app.get("/division-list", response_model=List[Division])
async def get_division_list(db: DataHelper = Depends(get_db)):
    result = await db.read_clob("Get_ODM_Data_Pkg.Get_Division_List")
    return json.loads(result)

@app.get("/division-summary", response_model=List[DivisionSummary])
async def get_division_summary(db: DataHelper = Depends(get_db)):
    result = await db.read_clob("Get_ODM_Data_Pkg.Get_Division_Summary_Data")
    return json.loads(result)

@app.get("/well-summary", response_model=List[WellSummary])
async def get_well_summary(well_id: int, division_id: int, db: DataHelper = Depends(get_db)):
    result = await db.read_clob("Get_ODM_Data_Pkg.Get_Well_Summary_Data", [well_id, division_id])
    return json.loads(result)

@app.get("/well-summary-by-day", response_model=List[WellSummaryByDay])
async def get_well_summary_by_day(well_id: int, division_id: int, db: DataHelper = Depends(get_db)):
    result = await db.read_cursor("Get_ODM_Data_Pkg.Get_Well_Summary_By_Day", [well_id, division_id])
    return result
