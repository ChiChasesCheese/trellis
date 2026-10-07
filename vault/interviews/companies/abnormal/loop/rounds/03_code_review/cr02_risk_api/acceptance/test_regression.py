"""Behaviour that must keep working after the fixes."""
import pytest
from riskapi_helpers import ACME_KEY, GLOBEX_KEY, World

pytestmark = pytest.mark.regression


def test_own_tenant_risk_is_served_and_cached():
    w = World()
    status, body = w.client.get("/tenants/acme/users/u1/risk", ACME_KEY)
    assert status == 200 and body["score"] == 70 and body["level"] == "high"
    assert [f["kind"] for f in body["factors"]] == ["mass_download", "impossible_travel"]
    assert len(w.cache.keys()) == 1
    assert w.client.get("/tenants/acme/users/u1/risk", ACME_KEY)[1]["computed_at"] == body["computed_at"]


def test_missing_or_wrong_key_is_401():
    w = World()
    assert w.client.get("/tenants/acme/users/u1/risk")[0] == 401
    assert w.client.get("/tenants/acme/users/u1/risk", "k_acme.wrong")[0] == 401
    assert w.client.get("/tenants/acme/users", "garbage")[0] == 401


def test_unknown_user_is_404():
    assert World().client.get("/tenants/acme/users/nobody/risk", ACME_KEY)[0] == 404


def test_list_orders_by_documented_columns():
    w = World()
    _s, by_name = w.client.get("/tenants/acme/users", ACME_KEY, sort="name")
    assert [i["name"] for i in by_name["items"]] == ["Ann", "Bob", "Cy", "Di", "Eve"]
    _s, by_score = w.client.get("/tenants/acme/users", ACME_KEY, sort="risk_score")
    scores = [i["risk_score"] for i in by_score["items"]]
    assert scores == sorted(scores)


def test_second_tenant_sees_only_its_own_users():
    w = World()
    _s, body = w.client.get("/tenants/globex/users", GLOBEX_KEY)
    assert [i["name"] for i in body["items"]] == ["Zed"]
