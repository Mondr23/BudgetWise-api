from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/cheapest-cities")
def cheapest_cities():

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
def expensive_cities():

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
def best_weather():

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
def top_tourism():

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
def best_budget():

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
def travel_value():

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
def healthy_cities():

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
def top_destinations():

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