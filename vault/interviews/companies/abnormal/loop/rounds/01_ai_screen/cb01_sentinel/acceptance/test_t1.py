"""t1 -- rule suppression. Only POST/GET/DELETE /suppressions are new; everything else is existing API."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cb01_support import DE, SG, build_env, travel  # noqa: E402

pytestmark = pytest.mark.t1


@pytest.fixture
def env(codebase_root_path, tmp_path):
    return build_env(codebase_root_path, tmp_path)


def create(env, tenant, body):
    resp = env.client(tenant).post("/suppressions", body)
    assert resp.status_code in (200, 201), resp.json
    return resp


def suppression_id(resp):
    data = resp.json
    if "id" not in data:  # tolerate {"suppression": {...}}
        data = next(v for v in data.values() if isinstance(v, dict) and "id" in v)
    return data["id"]


def listed(env, tenant):
    data = env.client(tenant).get("/suppressions").json
    return data if isinstance(data, list) else next(v for v in data.values() if isinstance(v, list))


@pytest.mark.regression
def test_without_suppressions_travel_alerts(env):
    env.ingest("acme", travel("acme", "alice@acme.test"))
    assert len(env.alerts("acme", rule="impossible_travel")) == 1


@pytest.mark.core
def test_rule_id_alone_silences_the_whole_rule(env):
    create(env, "acme", {"rule_id": "impossible_travel"})
    env.ingest("acme", travel("acme", "alice@acme.test", via=DE), travel("acme", "bob@acme.test", via=SG))
    assert env.alerts("acme", rule="impossible_travel") == []


@pytest.mark.core
def test_match_on_geo_country_suppresses_that_country(env):
    create(env, "acme", {"rule_id": "impossible_travel", "match": {"geo.country": "DE"}})
    env.ingest("acme", travel("acme", "alice@acme.test", via=DE))
    assert env.alerts("acme", rule="impossible_travel") == []


@pytest.mark.core
def test_non_matching_condition_still_alerts(env):
    create(env, "acme", {"rule_id": "impossible_travel", "match": {"geo.country": "DE"}})
    env.ingest("acme", travel("acme", "alice@acme.test", via=DE), travel("acme", "bob@acme.test", via=SG))
    alerts = env.alerts("acme", rule="impossible_travel")
    assert len(alerts) == 1  # the Singapore travel is not covered by the DE exception


@pytest.mark.core
def test_other_tenants_are_unaffected_and_cannot_see_it(env):
    sid = suppression_id(create(env, "globex", {"rule_id": "impossible_travel"}))
    env.ingest("acme", travel("acme", "alice@acme.test"))
    assert len(env.alerts("acme", rule="impossible_travel")) == 1
    assert listed(env, "acme") == []
    assert env.client("acme").delete(f"/suppressions/{sid}").status_code == 404
    assert [s["id"] for s in listed(env, "globex")] == [sid]  # still there


@pytest.mark.core
def test_invalid_rule_id_is_a_400_in_the_standard_error_shape(env):
    bad = env.client("acme").post("/suppressions", {"rule_id": "no_such_rule"})
    missing = env.client("acme").post("/suppressions", {"match": {"geo.country": "DE"}})
    assert bad.status_code == 400 and missing.status_code == 400
    reference = env.client("acme").get("/alerts/does-not-exist").json  # the existing error shape
    assert set(bad.json) == set(reference) == {"error"}
    assert set(bad.json["error"]) >= {"code", "message"}
    assert listed(env, "acme") == []


@pytest.mark.core
def test_list_and_delete_roundtrip_restores_alerting(env):
    sid = suppression_id(create(env, "acme", {"rule_id": "impossible_travel"}))
    assert [s["rule_id"] for s in listed(env, "acme")] == ["impossible_travel"]
    env.ingest("acme", travel("acme", "alice@acme.test"))
    assert env.alerts("acme", rule="impossible_travel") == []

    assert env.client("acme").delete(f"/suppressions/{sid}").status_code in (200, 204)
    assert listed(env, "acme") == []
    assert env.client("acme").delete(f"/suppressions/{sid}").status_code == 404
    env.ingest("acme", travel("acme", "bob@acme.test"))
    assert len(env.alerts("acme", rule="impossible_travel")) == 1


@pytest.mark.regression
def test_suppression_requires_authentication(env):
    from sentinel.api.testing import TestClient

    anon = TestClient(env.app.wsgi)
    assert anon.post("/suppressions", {"rule_id": "impossible_travel"}).status_code == 401
    assert anon.get("/suppressions").status_code == 401


@pytest.mark.stretch
def test_other_rules_on_the_same_event_still_alert(env):
    create(env, "acme", {"rule_id": "impossible_travel"})
    env.ingest("acme", travel("acme", "alice@acme.test"))  # also a first login from a new country
    assert env.alerts("acme", rule="impossible_travel") == []
    assert len(env.alerts("acme", rule="new_country_login")) == 1


@pytest.mark.stretch
def test_several_suppressions_for_one_rule_combine(env):
    create(env, "acme", {"rule_id": "impossible_travel", "match": {"geo.country": "DE"}})
    create(env, "acme", {"rule_id": "impossible_travel", "match": {"geo.country": "SG"}})
    env.ingest("acme", travel("acme", "alice@acme.test", via=DE), travel("acme", "bob@acme.test", via=SG))
    assert env.alerts("acme", rule="impossible_travel") == []


@pytest.mark.regression
def test_ack_flow_is_unchanged(env):
    env.ingest("acme", travel("acme", "alice@acme.test"))
    client = env.client("acme")
    alert = env.alerts("acme")[0]
    assert client.post(f"/alerts/{alert['id']}/ack").status_code == 200
    assert client.get(f"/alerts/{alert['id']}").json["status"] == "ACKED"
