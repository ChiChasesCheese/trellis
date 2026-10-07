"""HTTP API, driven through TestClient."""
from rulelang.api.testing import TestClient


def _seed(app, events_dir):
    app.pipeline.ingest_dir(events_dir, "acme")
    app.pipeline.ingest_dir(events_dir, "globex")


def test_requires_token(app):
    assert TestClient(app.wsgi).get("/signals").status_code == 401
    r = TestClient(app.wsgi, token="nope").get("/signals")
    assert r.status_code == 401 and r.json["error"]["code"] == "unauthorized"


def test_signals_for_one_event(app, acme, events_dir):
    _seed(app, events_dir)
    body = acme.get("/signals", params={"event_id": "a-010"}).json
    assert [(s["detector"], s["severity"]) for s in body["items"]] == [("new_sender", "low"), ("suspicious_link", "high")]
    assert set(body["items"][0]) == {"event_id", "detector", "severity", "summary", "evidence"}


def test_unknown_event_is_404_and_other_tenants_events_are_invisible(app, acme, globex, events_dir):
    _seed(app, events_dir)
    assert acme.get("/signals", params={"event_id": "nope"}).status_code == 404
    assert globex.get("/signals", params={"event_id": "a-010"}).status_code == 404


def test_list_is_tenant_scoped_and_limited(app, acme, globex, events_dir):
    _seed(app, events_dir)
    mine = acme.get("/signals", params={"limit": 3}).json
    assert len(mine["items"]) == 3
    assert all(s["event_id"].startswith(("a-", "c-")) for s in acme.get("/signals", params={"limit": 100}).json["items"])
    assert all(s["event_id"].startswith("g-") for s in globex.get("/signals").json["items"])


def test_bad_limit_is_a_400(acme):
    assert acme.get("/signals", params={"limit": "x"}).status_code == 400
    assert acme.get("/nope").status_code == 404
