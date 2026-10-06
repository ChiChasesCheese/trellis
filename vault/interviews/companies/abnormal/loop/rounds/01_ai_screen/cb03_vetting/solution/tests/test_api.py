from vetting.api.app import create_app
from vetting.api.testing import TestClient


def by_name(client, name):
    items = client.get("/reviews").json()["items"]
    return next(i for i in items if i["display_name"] == name)


def test_requires_a_valid_bearer_token(ingested):
    app = create_app(ingested)
    for token in (None, "nope"):
        response = TestClient(app, token=token).get("/reviews")
        assert response.status == 401 and response.json()["error"]["code"] == "unauthorized"


def test_list_is_ranked_and_filterable_by_tier(client):
    everything = client.get("/reviews").json()
    assert everything["count"] == 16
    scores = [i["score"] for i in everything["items"]]
    assert scores == sorted(scores, reverse=True)
    high = client.get("/reviews", recommendation="highly_recommended").json()
    assert [i["display_name"] for i in high["items"]] == ["Kai Mismatchwood", "Riley Sample"]
    bad = client.get("/reviews", recommendation="maybe")
    assert bad.status == 400 and bad.json()["error"]["code"] == "invalid_filter"


def test_detail_has_findings_citations_and_timeline(client):
    item = by_name(client, "Kai Mismatchwood")
    detail = client.get(f"/reviews/{item['identity_id']}").json()
    assert detail["recommendation"] == "HIGHLY_RECOMMENDED" and detail["disposition"] is None
    assert all(c["source"] and c["ref"] and c["ts"] for f in detail["findings"] for c in f["evidence"])
    assert detail["timeline"][0]["text"] == "Application received via Greenhouse"


def test_unknown_identity_and_route_use_the_error_shape(client):
    assert client.get("/reviews/greenhouse:nope").status == 404
    assert client.get("/reviews/greenhouse:nope").json()["error"]["code"] == "not_found"
    assert client.get("/nothing").status == 404
    assert client.delete("/reviews").status == 405


def test_tenants_are_isolated(ingested):
    other = TestClient(create_app(ingested), token="tok-globex-reviewer")
    assert other.get("/reviews").json()["count"] == 0
    assert other.get("/reviews/greenhouse:40120").status == 404


def test_disposition_is_recorded_validated_and_kept_as_history(client):
    path = "/reviews/greenhouse:40102"
    assert client.post(path + "/disposition", json={"decision": "maybe"}).status == 400
    assert client.post(path + "/disposition", json={"decision": "escalated", "note": "call"}).status == 201
    assert client.post(path + "/disposition", json={"decision": "cleared", "note": "verified"}).status == 201
    detail = client.get(path).json()
    assert detail["disposition"] == "cleared"
    assert [d["decision"] for d in detail["dispositions"]] == ["escalated", "cleared"]
    assert client.post("/reviews/greenhouse:nope/disposition", json={"decision": "cleared"}).status == 404
