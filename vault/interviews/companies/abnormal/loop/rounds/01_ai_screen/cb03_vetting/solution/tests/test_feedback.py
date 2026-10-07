from vetting.api.app import create_app
from vetting.api.testing import TestClient

from conftest import gh_record, ingest, write_json

VPN_A, VPN_B, VPN_C = "203.0.113.31", "203.0.113.32", "203.0.113.33"


def setup(tmp_path, db_path, records, tenant="acme"):
    write_json(tmp_path / "greenhouse/applications/a.json", records)
    ingest(db_path, tenant, tmp_path)
    token = {"acme": "tok-acme-reviewer", "globex": "tok-globex-reviewer"}[tenant]
    return TestClient(create_app(db_path), token=token)


def test_cleared_vpn_asn_softens_the_next_lone_vpn_candidate(tmp_path, db_path):
    client = setup(tmp_path, db_path, [gh_record(1, "Ann", "Alpha", "(206) 555-0101", VPN_A)])
    assert client.get("/reviews/greenhouse:1").json()["recommendation"] == "RECOMMENDED"
    client.post("/reviews/greenhouse:1/disposition", json={"decision": "cleared", "note": "corporate VPN"})
    write_json(tmp_path / "greenhouse/applications/b.json", [gh_record(2, "Bob", "Beta", "(312) 555-0102", VPN_B)])
    client = setup(tmp_path, db_path, [gh_record(1, "Ann", "Alpha", "(206) 555-0101", VPN_A)])
    detail = client.get("/reviews/greenhouse:2").json()
    assert detail["recommendation"] == "NONE"
    (found,) = detail["findings"]
    assert found["signal"] == "vpn_hosting_ip" and found["evidence"]
    assert "previously cleared by reviewer" in found["annotations"]
    assert [d["decision"] for d in client.get("/reviews/greenhouse:1").json()["dispositions"]] == ["cleared"]


def test_escalated_value_is_never_softened(tmp_path, db_path):
    client = setup(
        tmp_path,
        db_path,
        [gh_record(1, "Ann", "Alpha", "(206) 555-0101", VPN_A), gh_record(3, "Eve", "Gamma", "(404) 555-0103", VPN_C)],
    )
    client.post("/reviews/greenhouse:1/disposition", json={"decision": "cleared"})
    client.post("/reviews/greenhouse:3/disposition", json={"decision": "escalated"})
    client = setup(tmp_path, db_path, [gh_record(2, "Bob", "Beta", "(312) 555-0102", VPN_B)])
    assert client.get("/reviews/greenhouse:2").json()["recommendation"] == "RECOMMENDED"


def test_strong_combinations_and_other_tenants_are_unaffected(tmp_path, db_path):
    client = setup(tmp_path, db_path, [gh_record(1, "Ann", "Alpha", "(206) 555-0101", VPN_A)])
    client.post("/reviews/greenhouse:1/disposition", json={"decision": "cleared"})
    strong = gh_record(4, "Dee", "Delta", "+1 646 555 0102", VPN_B, resume_name="Dea Deltoid")
    client = setup(tmp_path, db_path, [gh_record(2, "Bob", "Beta", "(312) 555-0102", VPN_B), strong])
    assert client.get("/reviews/greenhouse:4").json()["recommendation"] == "HIGHLY_RECOMMENDED"
    other = setup(tmp_path, db_path, [gh_record(2, "Bob", "Beta", "(312) 555-0102", VPN_B)], tenant="globex")
    assert other.get("/reviews/greenhouse:2").json()["recommendation"] == "RECOMMENDED"
