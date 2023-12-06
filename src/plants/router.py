from typing import Any

from fastapi import APIRouter, Depends, Query

from src.database import execute_raw
from src.plants.database import plant_t,annual_emissions_t, PlantDataEnum as plant, PlantAnnualEmissionsEnum as emissions
from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import JWTData


router = APIRouter()


@router.get("/net_generation")
async def get_plants_net_generation(
    state_filter: str = Query(None, description="Filter by state abbreviation"),
    top_n: int = Query(None, description="Limit number of records"),
    detail: bool = Query(False, description="Include detailed plant information"),
    _: JWTData = Depends(parse_jwt_user_data),
):
    query: str = ""
    columns: str = "*"

    if not detail:
        columns = f""" 
            "{plant.plant_name}", 
            "{plant.plant_net_generation}",
            "{plant.plant_latitude}",
            "{plant.plant_longitude}",
            "{plant.plant_state_abbreviation}"
        """ 
    
    query = f"SELECT {columns} FROM \"{plant_t.name}\" AS p " 
    query += f"JOIN {annual_emissions_t.name} as e ON p.id = e.plant_fk " if detail else ""
    query += f"WHERE \"{plant.plant_net_generation}\" IS NOT NULL "
    query += f"AND \"{plant.plant_state_abbreviation}\" = '{state_filter}' " if state_filter else ""
    query += f"ORDER BY \"{plant.plant_net_generation}\" DESC "
    query += f"LIMIT {top_n}" if top_n else ""
    
    return await execute_raw(query)


@router.get("/state_aggegate")
async def actual_and_percentage_of_state_net_generation(
    top_n: int = Query(None, description="Limit number of records"),
    order: bool = Query(None, description="Order by state net generation"),
    _: JWTData = Depends(parse_jwt_user_data),
):
    LIMIT  = f"LIMIT {top_n}" if top_n else ""
    ORDER_BY = "ORDER BY state_total_generation DESC" if order else ""
    
    query = f"""
    SELECT 
        "{plant.plant_state_abbreviation}" AS state,
        SUM("{plant.plant_net_generation}") AS state_total_generation,
        SUM("{plant.plant_net_generation}") * 100.0 / SUM(SUM("{plant.plant_net_generation}")) OVER () AS state_percentage
    FROM  
        plant_data 
    GROUP BY state
    {ORDER_BY}
    {LIMIT} 
    ;
    """
    return await execute_raw(query)
