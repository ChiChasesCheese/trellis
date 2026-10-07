"""HTTP API, driven through TestClient."""
from sentinel.api.testing import TestClient


def _seed(app, events_dir):
    app.pipeline.ingest_dir(events_dir, "acme")
    app.pipeline.ingest_dir(events_dir, "globex")


def test_requires_token(app):
    assert TestClient(app.wsgi).get("/alerts").status_code == 401
    r = TestClient(app.wsgi, token="nope").get("/alerts")
    assert r.status_code == 401 and r.json["error"]["code"] == "unauthorized"


def test_list_alerts_sorted_by_score_and_paginated(app, acme, events_dir):
    _seed(app, events_dir)
    body = acme.get("/alerts").json
    scores = [a["score"] for a in body["items"]]
    assert scores == sorted(scores, reverse=True) and body["total"] == len(body["items"]) > 3
    page = acme.get("/alerts", params={"limit": 2, "offset": 1}).json
    assert [a["id"] for a in page["items"]] == [a["id"] for a in body["items"][1:3]]


def test_tenants_only_see_their_alerts(app, acme, globex, events_dir):
    _seed(app, events_dir)
    mine = {a["id"] for a in acme.get("/alerts").json["items"]}
    theirs = {a["id"] for a in globex.get("/alerts").json["items"]}
    assert mine and theirs and not (mine & theirs)
    assert globex.get(f"/alerts/{next(iter(mine))}").status_code == 404


def test_ack_flow(app, acme, events_dir):
    _seed(app, events_dir)
    alert_id = acme.get("/alerts").json["items"][0]["id"]
    assert acme.post(f"/alerts/{alert_id}/ack").json["status"] == "ACKED"
    open_ids = {a["id"] for a in acme.get("/alerts", params={"status": "open"}).json["items"]}
    assert alert_id not in open_ids


def test_validation_errors_use_the_standard_shape(acme):
    r = acme.get("/alerts", params={"limit": "abc"})
    assert r.status_code == 400 and r.json["error"]["code"] == "bad_request"
    assert acme.get("/alerts", params={"status": "weird"}).status_code == 400
    assert acme.get("/nope").json["error"]["code"] == "not_found"
    assert acme.post("/alerts").status_code == 405


def test_event_lookup_includes_enrichment(app, acme, events_dir):
    _seed(app, events_dir)
    body = acme.get("/events/a-003").json
    assert body["enrichment"]["geo"]["country"] == "SG"
    assert acme.get("/events/zzz").status_code == 404
