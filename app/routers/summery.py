from fastapi import APIRouter, HTTPException, Query
from app.database import SessionLocal
from app.models.city import City
from app.models.country import Country
from app.models.weather import Weather
from app.models.travel_cost import TravelCost
from app.models.review import Review
from app.models.tourism import Tourism  

router = APIRouter(prefix="/destinations", tags=["Destinations"])


@router.get("/summary")
def get_destination_summary(
    city: str = Query(None),
    country: str = Query(None)
):
    db = SessionLocal()

    if not city and not country:
        raise HTTPException(
            status_code=400,
            detail="Provide either city or country"
        )

    results = []

    # ------------------------
    #  CITY MODE
    # ------------------------
    if city:
        city_obj = db.query(City).filter(
            City.city_name.ilike(city)
        ).first()

        if not city_obj:
            db.close()
            raise HTTPException(status_code=404, detail="City not found")

        # --- TOURISM (LATEST YEAR) ---
        tourism = db.query(Tourism).filter(
            Tourism.country_code == city_obj.country_code
        ).order_by(Tourism.year.desc()).first()

        if tourism:
            tourism_info = f"{tourism.tourist_arrivals:,} visitors in {tourism.year}"
        else:
            tourism_info = "Tourism data not available"

        weather = db.query(Weather).filter(
            Weather.city_id == city_obj.city_id
        ).first()

        cost = db.query(TravelCost).filter(
            TravelCost.city_id == city_obj.city_id
        ).first()

        reviews = db.query(Review).filter(
            Review.city_id == city_obj.city_id
        ).all()

        # --- USER EXPERIENCE ---
        if reviews:
            user_experience = [
                {
                    "user": r.user_name,
                    "spent": r.money_spent,
                    "days": r.trip_days,
                    "rating": r.value_rating,
                    "comment": r.comment
                }
                for r in reviews
            ]
        else:
            user_experience = "No user reviews available"

        db.close()

        return {
            "city": city_obj.city_name,
            "country_code": city_obj.country_code,
            "tourism": tourism_info,  
            "weather": weather.condition if weather else None,
            "daily_cost": cost.daily_cost_estimate if cost else None,
            "user_experience": user_experience
        }

    # ------------------------
    #  COUNTRY MODE
    # ------------------------
    if country:
        country_obj = db.query(Country).filter(
            Country.country_name.ilike(country)
        ).first()

        if not country_obj:
            db.close()
            raise HTTPException(status_code=404, detail="Country not found")

        # --- TOURISM ---
        tourism = db.query(Tourism).filter(
            Tourism.country_code == country_obj.country_code
        ).order_by(Tourism.year.desc()).first()

        if tourism:
            tourism_info = f"{tourism.tourist_arrivals:,} visitors in {tourism.year}"
        else:
            tourism_info = "Tourism data not available"

        cities = db.query(City).filter(
            City.country_code == country_obj.country_code
        ).all()

        for city_obj in cities:

            weather = db.query(Weather).filter(
                Weather.city_id == city_obj.city_id
            ).first()

            cost = db.query(TravelCost).filter(
                TravelCost.city_id == city_obj.city_id
            ).first()

            reviews = db.query(Review).filter(
                Review.city_id == city_obj.city_id
            ).all()

            # --- USER EXPERIENCE ---
            if reviews:
                user_experience = [
                    {
                        "user": r.user_name,
                        "rating": r.value_rating,
                        "comment": r.comment
                    }
                    for r in reviews
                ]
            else:
                user_experience = "No user reviews available"

            results.append({
                "city": city_obj.city_name,
                "weather": weather.condition if weather else None,
                "daily_cost": cost.daily_cost_estimate if cost else None,
                "user_experience": user_experience
            })

        db.close()

        return {
            "country": country_obj.country_name,
            "tourism": tourism_info,  
            "cities": results
        }