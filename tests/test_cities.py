import pytest
from fastapi.testclient import TestClient
from app.main import app

# create test client
client = TestClient(app)


# -------------------------
# HELPER TOKENS
# -------------------------

# login as admin and return token
def get_admin_token():
    response = client.post("/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    return response.json()["access_token"]


# login as normal user
def get_user_token():
    response = client.post("/auth/login", json={
        "username": "user",
        "password": "user123"
    })
    return response.json()["access_token"]


# -------------------------
# PUBLIC ENDPOINT TESTS
# -------------------------

# should return all cities
def test_get_all_cities():
    response = client.get("/cities/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# invalid id should return 404
def test_get_city_not_found():
    response = client.get("/cities/999999")
    assert response.status_code == 404


# get cities by country code
def test_get_cities_by_country():
    response = client.get("/cities/country/GB")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# -------------------------
# CREATE CITY TESTS
# -------------------------

# no token → should be blocked
def test_create_city_no_token():
    response = client.post("/cities/", json={
        "city_name": "Test City",
        "country_code": "TC"
    })

    assert response.status_code in [401, 403]


# normal user should not be allowed
def test_create_city_as_user_forbidden():
    token = get_user_token()

    response = client.post(
        "/cities/",
        json={
            "city_name": "User City",
            "country_code": "UC"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [401, 403]


# admin can create city successfully
def test_create_city_admin_success():
    token = get_admin_token()

    import uuid
    unique_name = f"Admin City {uuid.uuid4()}"  # avoid duplicates

    response = client.post(
        "/cities/",
        json={
            "city_name": unique_name,
            "country_code": "AC"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


# creating same city twice should fail
def test_create_duplicate_city():
    token = get_admin_token()

    client.post(
        "/cities/",
        json={"city_name": "Duplicate City", "country_code": "DC"},
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.post(
        "/cities/",
        json={"city_name": "Duplicate City", "country_code": "DC"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400


# -------------------------
# UPDATE CITY TESTS
# -------------------------

# admin updates city name
def test_update_city_admin():
    token = get_admin_token()

    import uuid

    # create a city first
    create = client.post(
        "/cities/",
        json={
            "city_name": f"Update Me {uuid.uuid4()}",
            "country_code": "UM"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    city_id = create.json()["city_id"]

    new_name = f"Updated {uuid.uuid4()}"  # avoid conflicts

    response = client.put(
        f"/cities/{city_id}",
        params={"city_name": new_name},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


# updating non-existing city should fail
def test_update_city_not_found():
    token = get_admin_token()

    response = client.put(
        "/cities/999999",
        params={"city_name": "DoesNotExist"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


# no token → should not allow update
def test_update_city_no_token():
    response = client.put(
        "/cities/1",
        params={"city_name": "Fail"}
    )

    assert response.status_code in [401, 403]


# -------------------------
# DELETE CITY TESTS
# -------------------------

# admin deletes a city
def test_delete_city_admin():
    token = get_admin_token()

    # create city first
    create = client.post(
        "/cities/",
        json={"city_name": "Delete Me", "country_code": "DM"},
        headers={"Authorization": f"Bearer {token}"}
    )

    city_id = create.json()["city_id"]

    response = client.delete(
        f"/cities/{city_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


# deleting non-existing city
def test_delete_city_not_found():
    token = get_admin_token()

    response = client.delete(
        "/cities/999999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


# no token → should not allow delete
def test_delete_city_no_token():
    response = client.delete("/cities/1")

    assert response.status_code in [401, 403]