from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app.models.city import City
from app.schemas.city_schema import CityCreate
from app.auth.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get("/")
def get_cities():
    """
    Get all cities (public)
    """

    db = SessionLocal()
    cities = db.query(City).all()
    db.close()

    return cities


@router.get("/{city_id}")
def get_city(city_id: int):
    """
    Get city by ID
    """

    db = SessionLocal()
    city = db.query(City).filter(City.city_id == city_id).first()
    db.close()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.get("/country/{country_code}")
def get_cities_by_country(country_code: str):
    """
    Get all cities in a country
    """

    db = SessionLocal()
    cities = db.query(City).filter(City.country_code == country_code).all()
    db.close()

    return cities


@router.post("/")
def create_city(
    city: CityCreate,
    user=Depends(get_current_user)
):
    """
    Create city (ADMIN ONLY)
    """

    require_admin(user)

    db = SessionLocal()

    city_name = city.city_name.strip()
    country_code = city.country_code.upper()

    # Check duplicates
    existing = db.query(City).filter(
        City.city_name == city_name,
        City.country_code == country_code
    ).first()

    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="City already exists")

    new_city = City(
        city_name=city_name,
        country_code=country_code
    )

    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    db.close()

    return new_city


@router.put("/{city_id}")
def update_city(
    city_id: int,
    city_name: str,
    user=Depends(get_current_user)
):
    """
    Update city (ADMIN ONLY)
    """

    require_admin(user)

    db = SessionLocal()

    city = db.query(City).filter(City.city_id == city_id).first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    city.city_name = city_name.strip()

    db.commit()
    db.close()

    return {"message": "City updated"}


@router.delete("/{city_id}")
def delete_city(
    city_id: int,
    user=Depends(get_current_user)
):
    """
    Delete city (ADMIN ONLY)
    """

    require_admin(user)

    db = SessionLocal()

    city = db.query(City).filter(City.city_id == city_id).first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()
    db.close()

    return {"message": "City deleted"}