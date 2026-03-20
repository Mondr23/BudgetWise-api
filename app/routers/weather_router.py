from fastapi import APIRouter
from app.database import SessionLocal
from app.models.weather import Weather

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/")
def get_all_weather():

    db = SessionLocal()

    weather = db.query(Weather).all()

    db.close()

    return weather

# Get weather data for a specific city by city_id
@router.get("/{city_id}")
def get_weather(city_id: int):

    db = SessionLocal()

    weather = db.query(Weather).filter(
        Weather.city_id == city_id
    ).all()

    db.close()

    return weather