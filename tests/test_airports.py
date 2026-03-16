from tests.conftest import client


def test_get_airports():
    """
    Tests:
        GET /airports/
    """

    response = client.get("/airports/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_airports_by_city():
    """
    Tests:
        GET /airports/city/{city_id}
    """

    response = client.get("/airports/city/1")

    assert response.status_code == 200