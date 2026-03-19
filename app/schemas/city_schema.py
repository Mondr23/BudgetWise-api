# Input validation for city

from pydantic import BaseModel, constr


class CityCreate(BaseModel):
    """
    Validates city input
    """

    city_name: constr(min_length=2, max_length=50)
    country_code: constr(min_length=2, max_length=3)

