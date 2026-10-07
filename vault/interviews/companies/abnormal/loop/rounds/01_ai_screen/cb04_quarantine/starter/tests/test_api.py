from __future__ import annotations

from quarantine.api.testing import TestClient


def test_requires_a_token(app):
    assert TestClient(app.wsgi).get("/reports").status_code == 401
    assert TestClient(app.wsgi, token="nope").get("/reports").status_code == 401


def test_unknown_route_is_404_with_error_shape(acme):
    resp = acme.get("/nothing")
    assert resp.status_code == 404
    assert resp.json["error"]["code"] == "not_found"


def test_post_report_returns_201_then_200_for_the_same_message(acme, make_payload):
    payload = make_payload()
    first = acme.post("/reports", payload)
    second = acme.post("/reports", payload)
    assert (first.status_code, second.status_code) == (201, 200)
    assert first.json["id"] == second.json["id"]


def test_get_report(acme, make_payload):
    created = acme.post("/reports", make_payload(links=["https://login-micros0ft.example/a"])).json
    body = acme.get(f"/reports/{created['id']}").json
    assert body["disposition"] == "QUARANTINE"
    assert body["status"] == "QUARANTINED"
    assert {v["analyzer"] for v in body["verdicts"]} == {
        "attachment_type", "display_name_spoof", "link_reputation", "sender_reputation",
    }


def test_get_unknown_report_is_404(acme):
    assert acme.get("/reports/rpt_missing").status_code == 404


def test_list_reports_for_the_callers_tenant(acme, globex, make_payload):
    acme.post("/reports", make_payload())
    acme.post("/reports", make_payload())
    globex.post("/reports", make_payload())
    body = acme.get("/reports").json
    assert body["total"] == 2 and len(body["items"]) == 2
    assert globex.get("/reports").json["total"] == 1


def test_list_validates_paging(acme):
    assert acme.get("/reports", params={"limit": 0}).status_code == 400
    assert acme.get("/reports", params={"limit": "x"}).status_code == 400


def test_release_flow(acme, app, make_payload):
    created = acme.post("/reports", make_payload(links=["https://login-micros0ft.example/a"])).json
    resp = acme.post(f"/reports/{created['id']}/release")
    assert resp.status_code == 200
    assert resp.json["status"] == "RELEASED"
    assert len(app.mailbox.calls_of("release")) == 1


def test_release_unknown_report_is_404(acme):
    assert acme.post("/reports/rpt_missing/release").status_code == 404


def test_body_must_be_a_json_object(acme):
    assert acme.post("/reports", ["not", "an", "object"]).status_code == 400
