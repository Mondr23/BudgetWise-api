from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.country import Country
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/countries", tags=["Countries"])


# -------------------------
# Get all countries
# -------------------------
@router.get("/")
def get_countries():
    db = SessionLocal()
    countries = db.query(Country).all()
    db.close()
    return countries



# -------------------------
# Get country by code
# -------------------------
@router.get("/code/{country_code}")
def get_country_by_code(country_code: str):
    db = SessionLocal()

    country = db.query(Country).filter(
        Country.country_code == country_code
    ).first()

    db.close()

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    return country


# -------------------------
# Create new country
# -------------------------
@router.post("/")
def create_country(country_name: str, country_code: str):

    db = SessionLocal()

    try:
        new_country = Country(
            country_name=country_name,
            country_code=country_code
        )

        db.add(new_country)
        db.commit()
        db.refresh(new_country)

        return new_country

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Country with this code already exists"
        )

    finally:
        db.close()