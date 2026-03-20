from fastapi import APIRouter
from app.database import SessionLocal
from app.models.tourism import Tourism

router = APIRouter(prefix="/tourism", tags=["Tourism"])


@router.get("/{country_code}")
def get_tourism(country_code: str):

    db = SessionLocal()

   # get all tourism records for this country
    tourism = db.query(Tourism).filter(
        Tourism.country_code == country_code
    ).all()

    db.close()

    return tourism