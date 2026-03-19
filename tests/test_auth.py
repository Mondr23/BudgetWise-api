import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# -------------------------
# TEST LOGIN SUCCESS
# -------------------------

# should return token for valid credentials
def test_login_success():
    response = client.post("/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })

    assert response.status_code == 200
    data = response.json()

    # check token exists
    assert "access_token" in data
    assert data["access_token"] is not None


# -------------------------
# TEST LOGIN FAILURE
# -------------------------

# wrong password should fail
def test_login_invalid_password():
    response = client.post("/auth/login", json={
        "username": "admin",
        "password": "wrongpassword"
    })

    assert response.status_code in [400, 401]


# wrong username should also fail
def test_login_invalid_user():
    response = client.post("/auth/login", json={
        "username": "not_a_user",
        "password": "admin123"
    })

    assert response.status_code in [400, 401]


# -------------------------
# TEST PROTECTED ACCESS
# -------------------------

# trying to access protected endpoint without token
def test_access_without_token():
    response = client.post("/cities/", json={
        "city_name": "NoAuth City",
        "country_code": "NA"
    })

    # should be unauthorized
    assert response.status_code in [401, 403]