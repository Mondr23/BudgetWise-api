"""
test_weather.py

Tests weather endpoints.
"""

from tests.conftest import client


def test_get_weather():
    """
    Tests:
        GET /weather/
    """

    response = client.get("/weather/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_weather_by_city():
    """
    Tests:
        GET /weather/{city_id}
    """

    response = client.get("/weather/1")

    assert response.status_code == 200