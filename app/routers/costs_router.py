from fastapi import APIRouter
from app.database import SessionLocal
from app.models.travel_cost import TravelCost

router = APIRouter(prefix="/travel-costs", tags=["Travel Costs"])


@router.get("/{city_id}")
def get_travel_cost(city_id: int):

    db = SessionLocal()

    cost = db.query(TravelCost).filter(
        TravelCost.city_id == city_id
    ).first()

    db.close()

    return cost