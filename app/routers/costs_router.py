from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.travel_cost import TravelCost
from app.models.city import City

router = APIRouter(prefix="/travel-costs", tags=["Travel Costs"])


# Get all travel costs
@router.get("/")
def get_travel_costs():
    db = SessionLocal()

    data = db.query(TravelCost).all()

    db.close()
    return data


# Get travel cost by city name
@router.get("/city/{city_name}")
def get_cost_by_city_name(city_name: str):
    db = SessionLocal()


    city = db.query(City).filter(
        City.city_name.ilike(city_name)
    ).first()

 # if city not found  return error
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    cost = db.query(TravelCost).filter(
        TravelCost.city_id == city.city_id
    ).first()

    db.close()

  # if no cost found  return error
    if not cost:
        raise HTTPException(status_code=404, detail="Travel cost not found")

    return cost

