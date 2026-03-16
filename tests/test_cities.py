from tests.conftest import client


def test_get_cities():
    """
    Ensures API returns a list of cities.
    """

    response = client.get("/cities/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_city():
    """
    Ensures a city can be created.
    """

    response = client.post(
        "/cities/",
        params={
            "city_name": "Tokyo",
            "country_code": "JP"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["city_name"] == "Tokyo"


def test_get_city():
    """
    Integration Test

    Flow:
        Create city -> retrieve city
    """

    create = client.post(
        "/cities/",
        params={
            "city_name": "Osaka",
            "country_code": "JP"
        }
    )

    city_id = create.json()["city_id"]

    response = client.get(f"/cities/{city_id}")

    assert response.status_code == 200
    assert response.json()["city_id"] == city_id


def test_update_city():
    """
    Tests updating a city using:

        PUT /cities/{id}
    """

    create = client.post(
        "/cities/",
        params={"city_name": "Kyoto", "country_code": "JP"}
    )

    city_id = create.json()["city_id"]

    response = client.put(
        f"/cities/{city_id}",
        params={"city_name": "Kyoto Updated"}
    )

    assert response.status_code == 200


def test_delete_city():
    """
    Tests deleting a city.
    """

    create = client.post(
        "/cities/",
        params={"city_name": "Nagoya", "country_code": "JP"}
    )

    city_id = create.json()["city_id"]

    response = client.delete(f"/cities/{city_id}")

    assert response.status_code == 200


def test_city_not_found():
    """
    Error Test

    Requesting an invalid city ID
    should return 404.
    """

    response = client.get("/cities/999999")

    assert response.status_code == 404