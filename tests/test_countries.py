import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


# -------------------------
# HELPER TOKENS
# -------------------------

# login as admin
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

# should return list of countries
def test_get_all_countries():
    response = client.get("/countries/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# invalid country code should return 404
def test_get_country_not_found():
    response = client.get("/countries/ZZZ")
    assert response.status_code == 404


# -------------------------
# CREATE COUNTRY TESTS
# -------------------------

# no token → should fail
def test_create_country_no_token():
    response = client.post("/countries/", json={
        "country_name": "Testland",
        "country_code": "TL"
    })

    assert response.status_code in [401, 403]


# normal user should not be allowed
def test_create_country_as_user_forbidden():
    token = get_user_token()

    response = client.post(
        "/countries/",
        json={
            "country_name": "Userland",
            "country_code": "UL"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [401, 403]


# admin can create country
def test_create_country_admin_success():
    token = get_admin_token()

    code = str(uuid.uuid4())[:3].upper()

    response = client.post(
        "/countries/",
        json={
            "country_name": "TestLand",
            "country_code": code
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


# duplicate country should fail
def test_create_duplicate_country():
    token = get_admin_token()

    client.post(
        "/countries/",
        json={"country_name": "DuplicateLand", "country_code": "DL"},
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.post(
        "/countries/",
        json={"country_name": "DuplicateLand", "country_code": "DL"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400


# -------------------------
# UPDATE COUNTRY TESTS
# -------------------------

# admin updates country name
def test_update_country_admin():
    token = get_admin_token()

    import uuid
    code = str(uuid.uuid4())[:2].upper()

    # create country first
    client.post(
        "/countries/",
        json={
            "country_name": f"OldName {code}",
            "country_code": code
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.put(
        f"/countries/{code}",
        params={"country_name": f"NewName {code}"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


# update non-existing country
def test_update_country_not_found():
    token = get_admin_token()

    response = client.put(
        "/countries/ZZZ",
        params={"country_name": "DoesNotExist"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


# no token → should fail
def test_update_country_no_token():
    response = client.put(
        "/countries/US",
        params={"country_name": "Fail"}
    )

    assert response.status_code in [401, 403]


# -------------------------
# DELETE COUNTRY TESTS
# -------------------------

# admin deletes country
def test_delete_country_admin():
    token = get_admin_token()

    import uuid
    code = str(uuid.uuid4())[:2].upper()

    # create first
    client.post(
        "/countries/",
        json={
            "country_name": f"DeleteMe {code}",
            "country_code": code
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.delete(
        f"/countries/{code}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


# delete non-existing country
def test_delete_country_not_found():
    token = get_admin_token()

    response = client.delete(
        "/countries/ZZZ",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


# no token → should fail
def test_delete_country_no_token():
    response = client.delete("/countries/US")

    assert response.status_code in [401, 403]