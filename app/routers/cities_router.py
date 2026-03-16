from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.city import City

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get("/")
def get_cities():
    db = SessionLocal()
    cities = db.query(City).all()
    db.close()
    return cities


@router.get("/{city_id}")
def get_city(city_id: int):
    db = SessionLocal()
    city = db.query(City).filter(City.city_id == city_id).first()
    db.close()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.get("/country/{country_code}")
def get_cities_by_country(country_code: str):
    db = SessionLocal()
    cities = db.query(City).filter(City.country_code == country_code).all()
    db.close()
    return cities


@router.post("/")
def create_city(city_name: str, country_code: str):

    db = SessionLocal()

    # Normalize values (good practice)
    city_name = city_name.strip()
    country_code = country_code.upper()

    # Check if city already exists in this country
    existing_city = db.query(City).filter(
        City.city_name == city_name,
        City.country_code == country_code
    ).first()

    if existing_city:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="City already exists in this country"
        )

    # Create new city
    city = City(
        city_name=city_name,
        country_code=country_code
    )

    db.add(city)
    db.commit()
    db.refresh(city)
    db.close()

    return city


@router.put("/{city_id}")
def update_city(city_id: int, city_name: str):

    db = SessionLocal()

    city = db.query(City).filter(City.city_id == city_id).first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    city.city_name = city_name

    db.commit()
    db.close()

    return {"message": "City updated"}


@router.delete("/{city_id}")
def delete_city(city_id: int):

    db = SessionLocal()

    city = db.query(City).filter(City.city_id == city_id).first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()
    db.close()

    return {"message": "City deleted"}