# ---------------------------------------------
# Test file for Reviews API
# Covers validation + user input + edge cases
# ---------------------------------------------

from tests.conftest import client


# -----------------------------
# CREATE VALID REVIEW
# -----------------------------
def test_create_review():
    res = client.post("/reviews/", params={
        "city_id": 1,
        "user_name": "Tester",
        "money_spent": 500,
        "trip_days": 5,
        "value_rating": 4,
        "comment": "Nice"
    })

    assert res.status_code == 200


# -----------------------------
# INVALID REVIEW (BAD RATING)
# -----------------------------
def test_invalid_review():
    res = client.post("/reviews/", params={
        "city_id": 1,
        "user_name": "Tester",
        "money_spent": 500,
        "trip_days": 5,
        "value_rating": 10,
        "comment": "Bad"
    })

    # Should fail validation
    assert res.status_code == 400


# -----------------------------
# GET REVIEWS BY CITY
# -----------------------------
def test_get_reviews():
    res = client.get("/reviews/city/1")

    assert res.status_code == 200