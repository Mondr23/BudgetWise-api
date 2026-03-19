from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.travel_cost import TravelCost

router = APIRouter(prefix="/travel-costs", tags=["Travel Costs"])


@router.get("/")
def get_travel_costs():
    db = SessionLocal()

    data = db.query(TravelCost).all()

    db.close()
    return data

@router.get("/city/{city_name}")
def get_cost_by_city_name(city_name: str):
    db = SessionLocal()

    from app.models.city import City

    city = db.query(City).filter(
        City.city_name.ilike(city_name)
    ).first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    cost = db.query(TravelCost).filter(
        TravelCost.city_id == city.city_id
    ).first()

    db.close()

    if not cost:
        raise HTTPException(status_code=404, detail="Travel cost not found")

    return cost

