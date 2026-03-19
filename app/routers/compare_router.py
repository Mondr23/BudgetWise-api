from fastapi import APIRouter, HTTPException, Query
from app.database import SessionLocal

from app.models.city import City
from app.models.weather import Weather
from app.models.travel_cost import TravelCost
from app.models.review import Review
from app.models.tourism import Tourism

router = APIRouter(prefix="/compare", tags=["Compare"])


@router.get("/cities")
def compare_cities(
    city1: str = Query(...),
    city2: str = Query(...)
):
    db = SessionLocal()

    def get_city_data(city_name):

        city_obj = db.query(City).filter(
            City.city_name.ilike(city_name)
        ).first()

        if not city_obj:
            return None

        # --- WEATHER ---
        weather = db.query(Weather).filter(
            Weather.city_id == city_obj.city_id
        ).first()

        # --- COST ---
        cost = db.query(TravelCost).filter(
            TravelCost.city_id == city_obj.city_id
        ).first()

        # --- TOURISM ---
        tourism = db.query(Tourism).filter(
            Tourism.country_code == city_obj.country_code
        ).order_by(Tourism.year.desc()).first()

        if tourism:
            tourism_info = f"{tourism.tourist_arrivals:,} visitors in {tourism.year}"
            tourism_value = tourism.tourist_arrivals
        else:
            tourism_info = "Tourism data not available"
            tourism_value = None

        # --- REVIEWS ---
        reviews = db.query(Review).filter(
            Review.city_id == city_obj.city_id
        ).all()

        if reviews:
            avg_rating = sum(r.value_rating for r in reviews) / len(reviews)
        else:
            avg_rating = None

        return {
            "city": city_obj.city_name,
            "country_code": city_obj.country_code,
            "weather": weather.condition if weather else None,
            "daily_cost": cost.daily_cost_estimate if cost else None,
            "tourism_value": tourism_value,
            "rating": round(avg_rating, 1) if avg_rating else None
        }

    c1 = get_city_data(city1)
    c2 = get_city_data(city2)

    if not c1 or not c2:
        db.close()
        raise HTTPException(status_code=404, detail="One or both cities not found")

    # --- WEATHER SCORE (SMART FIX 🔥) ---
    weather_score = {
        "Sunny": 3,
        "Cloudy": 2,
        "Rainy": 1
    }

    def compare(metric):
        v1 = c1.get(metric)
        v2 = c2.get(metric)

        if v1 is None or v2 is None:
            return "N/A"

        if metric == "daily_cost":
            return c1["city"] if v1 < v2 else c2["city"]

        if metric == "weather":
            w1 = weather_score.get(v1, 0)
            w2 = weather_score.get(v2, 0)
            return c1["city"] if w1 > w2 else c2["city"]

        if metric == "tourism_value":
            return c1["city"] if v1 > v2 else c2["city"]

        if metric == "rating":
            return c1["city"] if v1 > v2 else c2["city"]

        return "N/A"

    result = {
        "city1": c1,
        "city2": c2,
        "comparison": {
            "cheaper": compare("daily_cost"),
            "better_weather": compare("weather"),
            "more_tourism": compare("tourism_value"),
            "higher_rating": compare("rating")
        }
    }

    db.close()
    return result