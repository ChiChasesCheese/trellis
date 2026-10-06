from vetting.api.app import create_app
from vetting.settings import DEFAULT_CONFIG_DIR, load_settings
from vetting.api.testing import TestClient

from conftest import gh_record, ingest, write_json

TRIO = ("greenhouse:40111", "greenhouse:40112", "greenhouse:40113")


def finding(client, identity_id):
    detail = client.get(f"/reviews/{identity_id}").json()
    return detail, next((f for f in detail["findings"] if f["signal"] == "coordinated_applicants"), None)


def test_campaign_members_cite_each_other(client):
    for me in TRIO:
        detail, found = finding(client, me)
        assert found and detail["recommendation"] != "NONE"
        refs = " ".join(c["ref"] for c in found["evidence"])
        assert all(other in refs for other in TRIO if other != me)
    _, found = finding(client, TRIO[0])
    assert any(e["ref"].startswith(TRIO[1]) for e in finding(client, TRIO[0])[0]["timeline"])


def test_benign_overlaps_are_not_flagged(client):
    # 40106 and 40107 share only an office NAT address.
    for identity_id in ("greenhouse:40106", "greenhouse:40107", "greenhouse:40101"):
        assert finding(client, identity_id)[1] is None


def test_one_shared_kind_is_not_enough(tmp_path, db_path):
    write_json(
        tmp_path / "greenhouse/applications/a.json",
        [gh_record(1, "Ann", "Alpha", "(206) 555-0101", "198.51.100.5"), gh_record(2, "Bob", "Beta", "(206) 555-0102", "192.0.2.9")],
    )
    ingest(db_path, "acme", tmp_path)
    client = TestClient(create_app(db_path), token="tok-acme-reviewer")
    assert finding(client, "greenhouse:1")[1] is None


def test_phone_formats_and_ip_neighbours_link(tmp_path, db_path):
    write_json(
        tmp_path / "greenhouse/applications/a.json",
        [
            gh_record(1, "Ann", "Alpha", "(206) 555-0101", "198.51.100.40"),
            gh_record(2, "Bob", "Beta", "+1 206-555-0101 x12", "198.51.100.41"),
        ],
    )
    ingest(db_path, "acme", tmp_path)
    client = TestClient(create_app(db_path), token="tok-acme-reviewer")
    assert finding(client, "greenhouse:1")[1] and finding(client, "greenhouse:2")[1]


def test_allowlisted_network_does_not_count(tmp_path, db_path):
    cfg = tmp_path / "config"
    (cfg / "tenants").mkdir(parents=True)
    text = (DEFAULT_CONFIG_DIR / "default.toml").read_text().replace("allowlist_cidrs = []", 'allowlist_cidrs = ["198.51.100.0/24"]')
    (cfg / "default.toml").write_text(text)
    assert load_settings("acme", cfg).correlation.allowlist_cidrs == ("198.51.100.0/24",)
    write_json(
        tmp_path / "in/greenhouse/applications/a.json",
        [gh_record(1, "Ann", "Alpha", "(206) 555-0101", "198.51.100.40"), gh_record(2, "Bob", "Beta", "(206) 555-0102", "198.51.100.41")],
    )
    from vetting.pipeline import Pipeline
    from vetting.store import Store

    store = Store.open(db_path)
    Pipeline.for_tenant("acme", store, config_dir=cfg).ingest(tmp_path / "in")
    # phone block + allowlisted /24: only one kind remains, so no link
    assert all(not r.findings for r in store.reviews.list("acme"))
    store.close()


def test_other_tenant_is_not_correlated(tmp_path, db_path):
    one, two = tmp_path / "one", tmp_path / "two"
    write_json(one / "greenhouse/applications/a.json", [gh_record(1, "Ann", "Alpha", "(206) 555-0101", "198.51.100.40", digest="f" * 64)])
    write_json(two / "greenhouse/applications/a.json", [gh_record(2, "Bob", "Beta", "(206) 555-0101", "198.51.100.40", digest="f" * 64)])
    ingest(db_path, "acme", one)
    ingest(db_path, "globex", two)
    for tenant, token, ident in (("acme", "tok-acme-reviewer", "greenhouse:1"), ("globex", "tok-globex-reviewer", "greenhouse:2")):
        assert finding(TestClient(create_app(db_path), token=token), ident)[1] is None
