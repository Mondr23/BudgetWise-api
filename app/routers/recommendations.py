from fastapi import APIRouter, HTTPException, Query
from app.database import SessionLocal
from app.models.city import City
from app.models.travel_cost import TravelCost
from app.models.weather import Weather
from app.models.review import Review
from app.models.tourism import Tourism  

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/best-destination")
def best_destination(
    budget: float = Query(...),
    days: int = Query(...),
    weather_pref: str = Query(None)
):
    db = SessionLocal()

    results = []

    cities = db.query(City).all()

    for city in cities:

        # --- GET COST ---
        cost = db.query(TravelCost).filter(
            TravelCost.city_id == city.city_id
        ).first()

        if not cost:
            continue

        daily_cost = cost.daily_cost_estimate
        estimated_trip_cost = daily_cost * days

        #  skip if over budget
        if estimated_trip_cost > budget:
            continue

        # --- GET WEATHER ---
        weather = db.query(Weather).filter(
            Weather.city_id == city.city_id
        ).first()

        #  WEATHER FILTER
        if weather_pref:
            if not weather or weather.condition.lower() != weather_pref.lower():
                continue

        #  GET TOURISM 
        tourism = db.query(Tourism).filter(
            Tourism.country_code == city.country_code
        ).order_by(Tourism.year.desc()).first()

        if tourism:
            tourism_info = f"{tourism.tourist_arrivals:,} visitors in {tourism.year}"
        else:
            tourism_info = "Tourism data not available"

        # --- GET REVIEWS ---
        reviews = db.query(Review).filter(
            Review.city_id == city.city_id
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

        results.append({
            "city": city.city_name,
            "country_code": city.country_code,
            "estimated_trip_cost": round(estimated_trip_cost, 2),
            "weather": weather.condition if weather else None,
            "tourism": tourism_info,  
            "user_experience": user_experience
        })

    db.close()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No destinations match your filters"
        )

    return {
        "budget": budget,
        "days": days,
        "weather_filter": weather_pref,
        "recommended_destinations": results[:5]
    }