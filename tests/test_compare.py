# ---------------------------------------------
# Test file for Compare API
# Tests analytical comparison between cities
# ---------------------------------------------

from tests.conftest import client


def test_compare_cities():
    res = client.get("/compare/cities?city1=london&city2=madrid")

    assert res.status_code == 200

    data = res.json()

    # Ensure comparison object exists
    assert "comparison" in data