"""
test_analytics.py

Tests analytics endpoints.
"""

from tests.conftest import client


def test_cheapest_cities():
    response = client.get("/analytics/cheapest-cities")
    assert response.status_code == 200


def test_expensive_cities():
    response = client.get("/analytics/expensive-cities")
    assert response.status_code == 200


def test_best_weather():
    response = client.get("/analytics/best-weather")
    assert response.status_code == 200


def test_top_tourism():
    response = client.get("/analytics/top-tourism-countries")
    assert response.status_code == 200


def test_best_budget_destinations():
    response = client.get("/analytics/best-budget-destinations")
    assert response.status_code == 200


def test_travel_value_index():
    response = client.get("/analytics/travel-value-index")
    assert response.status_code == 200


def test_healthy_cities():
    response = client.get("/analytics/healthy-cheap-cities")
    assert response.status_code == 200


def test_top_destinations():
    response = client.get("/analytics/top-travel-destinations")
    assert response.status_code == 200