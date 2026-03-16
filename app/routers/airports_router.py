from fastapi import APIRouter
from app.database import SessionLocal
from app.models.airport import Airport

router = APIRouter(prefix="/airports", tags=["Airports"])


@router.get("/")
def get_airports():
    db = SessionLocal()
    airports = db.query(Airport).all()
    db.close()
    return airports


@router.get("/city/{city_id}")
def get_airports_by_city(city_id: int):

    db = SessionLocal()

    airports = db.query(Airport).filter(
        Airport.city_id == city_id
    ).all()

    db.close()

    return airports