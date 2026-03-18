from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from app.database import engine
from app.auth.api_key import verify_api_key
from app.core.limiter import limiter

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/cheapest-cities")
@limiter.limit("5/minute")
def cheapest_cities(request: Request, api_key=Depends(verify_api_key)):
    """
    Returns cheapest cities based on daily cost
    Protected by API key + rate limiting
    """

    query = """
    SELECT c.city_name, t.daily_cost_estimate
    FROM travel_costs t
    JOIN cities c ON t.city_id = c.city_id
    ORDER BY t.daily_cost_estimate ASC
    LIMIT 10
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]


@router.get("/expensive-cities")
@limiter.limit("5/minute")
def expensive_cities(request: Request, api_key=Depends(verify_api_key)):
    """
    Returns most expensive cities
    """

    query = """
    SELECT c.city_name, t.daily_cost_estimate
    FROM travel_costs t
    JOIN cities c ON t.city_id = c.city_id
    ORDER BY t.daily_cost_estimate DESC
    LIMIT 10
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]


@router.get("/best-weather")
@limiter.limit("5/minute")
def best_weather(request: Request, api_key=Depends(verify_api_key)):
    """
    Cities with best weather (highest temperature)
    """

    query = """
    SELECT c.city_name, w.temperature
    FROM weather w
    JOIN cities c ON w.city_id = c.city_id
    ORDER BY w.temperature DESC
    LIMIT 10
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]


@router.get("/top-tourism-countries")
@limiter.limit("5/minute")
def top_tourism(request: Request, api_key=Depends(verify_api_key)):
    """
    Countries with highest tourism numbers
    """

    query = """
    SELECT country_code, tourist_arrivals
    FROM tourism_statistics
    ORDER BY tourist_arrivals DESC
    LIMIT 10
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]


@router.get("/best-budget-destinations")
@limiter.limit("5/minute")
def best_budget(request: Request, api_key=Depends(verify_api_key)):
    """
    Best budget destinations with good weather
    """

    query = """
    SELECT c.city_name, w.temperature, t.daily_cost_estimate
    FROM cities c
    JOIN weather w ON c.city_id = w.city_id
    JOIN travel_costs t ON c.city_id = t.city_id
    WHERE w.temperature BETWEEN 18 AND 30
    ORDER BY t.daily_cost_estimate ASC
    LIMIT 10
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]


@router.get("/travel-value-index")
@limiter.limit("5/minute")
def travel_value(request: Request, api_key=Depends(verify_api_key)):
    """
    Value index = tourism / cost
    """

    query = """
    SELECT
    c.city_name,
    (tourist_arrivals / daily_cost_estimate) AS value_index
    FROM tourism_statistics ts
    JOIN countries co ON ts.country_code = co.country_code
    JOIN cities c ON c.country_code = co.country_code
    JOIN travel_costs tc ON tc.city_id = c.city_id
    ORDER BY value_index DESC
    LIMIT 10
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]


@router.get("/healthy-cheap-cities")
@limiter.limit("5/minute")
def healthy_cities(request: Request, api_key=Depends(verify_api_key)):
    """
    Cities with good air quality + low cost
    """

    query = """
    SELECT
    c.city_name,
    w.air_quality_pm25,
    t.daily_cost_estimate
    FROM cities c
    JOIN weather w ON c.city_id = w.city_id
    JOIN travel_costs t ON c.city_id = t.city_id
    WHERE w.air_quality_pm25 < 20
    ORDER BY t.daily_cost_estimate ASC
    LIMIT 10
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]


@router.get("/top-travel-destinations")
@limiter.limit("5/minute")
def top_destinations(request: Request, api_key=Depends(verify_api_key)):
    """
    Top destinations based on temperature
    """

    query = """
    SELECT
    c.city_name,
    w.temperature,
    t.daily_cost_estimate
    FROM cities c
    JOIN weather w ON c.city_id = w.city_id
    JOIN travel_costs t ON c.city_id = t.city_id
    ORDER BY w.temperature DESC
    LIMIT 10
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]