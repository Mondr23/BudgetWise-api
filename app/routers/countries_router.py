from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app.models.country import Country
from app.schemas.country_schema import CountrySchema
from app.auth.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/countries", tags=["Countries"])


# -------------------------
# Get all countries (public)
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
@router.get("/{country_code}")
def get_country(country_code: str):
    db = SessionLocal()

    country = db.query(Country).filter(
        Country.country_code == country_code.upper()
    ).first()

    db.close()

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    return country


# -------------------------
# Create country (ADMIN ONLY)
# -------------------------
@router.post("/")
def create_country(
    country: CountrySchema,
    user=Depends(require_admin)
):


    db = SessionLocal()

    country_name = country.country_name.strip().title()
    country_code = country.country_code.upper()

    # --- CHECK DUPLICATES ---
    existing = db.query(Country).filter(
        (Country.country_code == country_code) |
        (Country.country_name == country_name)
    ).first()

    if existing:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Country already exists"
        )

    new_country = Country(
        country_name=country_name,
        country_code=country_code
    )

    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    db.close()

    return new_country


# -------------------------
# Update country (ADMIN ONLY)
# -------------------------
@router.put("/{country_code}")
def update_country(
    country_code: str,
    country_name: str,
    user=Depends(require_admin)
):


    db = SessionLocal()

    country = db.query(Country).filter(
        Country.country_code == country_code.upper()
    ).first()

    if not country:
        db.close()
        raise HTTPException(status_code=404, detail="Country not found")

    country.country_name = country_name.strip().title()

    db.commit()
    db.close()

    return {"message": "Country updated"}


# -------------------------
# Delete country (ADMIN ONLY)
# -------------------------
@router.delete("/{country_code}")
def delete_country(
    country_code: str,
    user=Depends(require_admin)
):


    db = SessionLocal()

    country = db.query(Country).filter(
        Country.country_code == country_code.upper()
    ).first()

    if not country:
        db.close()
        raise HTTPException(status_code=404, detail="Country not found")

    db.delete(country)
    db.commit()
    db.close()

    return {"message": "Country deleted"}