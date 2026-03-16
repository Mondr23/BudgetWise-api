"""
test_tourism.py

Tests tourism endpoints.
"""

from tests.conftest import client


def test_tourism_by_country():
    """
    Tests:
        GET /tourism/{country_code}
    """

    response = client.get("/tourism/JP")

    assert response.status_code == 200