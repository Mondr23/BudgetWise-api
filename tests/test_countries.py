"""
test_countries.py

This file tests all endpoints related to COUNTRIES.

Testing includes:
1. API Endpoint Testing
2. Error Testing
3. Response Validation
"""

from tests.conftest import client


def test_get_countries():
    """
    API Endpoint Test

    This test checks if the endpoint:
        GET /countries/

    Returns:
        - status code 200
        - a list of countries
    """

    response = client.get("/countries/")

    # Check HTTP response status
    assert response.status_code == 200

    # Check response format is a list
    assert isinstance(response.json(), list)


def test_create_country():
    """
    API Endpoint Test

    This test verifies that we can create a country
    using the endpoint:

        POST /countries/
    """

    response = client.post(
        "/countries/",
        params={
            "country_code": "JP",
            "country_name": "Japan"
        }
    )

    assert response.status_code == 200

    data = response.json()

    # Validate returned data
    assert data["country_code"] == "JP"
    assert data["country_name"] == "Japan"


def test_get_country_by_code():
    """
    Integration Test

    This test ensures we can retrieve
    a country that was created earlier.
    """

    response = client.get("/countries/code/JP")

    assert response.status_code == 200
    assert response.json()["country_code"] == "JP"


def test_country_not_found():
    """
    Error Testing

    Requesting a non-existing country
    should return a 404 error.
    """

    response = client.get("/countries/code/XXX")

    assert response.status_code == 404