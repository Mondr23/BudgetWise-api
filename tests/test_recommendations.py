# ---------------------------------------------
# Test file for Recommendation API
# Tests intelligent destination suggestions
# ---------------------------------------------

from tests.conftest import client


# -----------------------------
# NORMAL RECOMMENDATION
# -----------------------------
def test_recommendation():
    res = client.get("/recommendations/best-destination?budget=1000&days=5")

    assert res.status_code == 200


# -----------------------------
# EDGE CASE: LOW BUDGET
# -----------------------------
def test_low_budget():
    res = client.get("/recommendations/best-destination?budget=1&days=5")

    # Could return empty result or handled case
    assert res.status_code in [200, 404]