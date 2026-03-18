from sqlalchemy import text
from app.database import engine


def get_cheapest_cities():

    query = """
    SELECT c.city_name, t.daily_cost_estimate
    FROM travel_costs t
    JOIN cities c ON t.city_id = c.city_id
    ORDER BY t.daily_cost_estimate ASC
    LIMIT 10
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row) for row in result]