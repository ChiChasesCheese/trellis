from vetting.api.app import create_app
from vetting.api.testing import TestClient
from vetting.metrics import metrics
from vetting.pipeline import Pipeline
from vetting.store import Store

from conftest import FIXTURES, ingest


def workday_root(tmp_path):
    import shutil

    shutil.copytree(FIXTURES / "workday", tmp_path / "workday")
    return tmp_path


def reviews(client):
    return {i["display_name"]: i for i in client.get("/reviews").json()["items"]}


def test_workday_ingest_follows_pages_and_dedupes(tmp_path, db_path):
    metrics.reset()
    ingest(db_path, "acme", workday_root(tmp_path))
    client = TestClient(create_app(db_path), token="tok-acme-reviewer")
    assert sorted(reviews(client)) == ["Dana Cleanfield", "Lee Nophone", "Pat Noemailson", "Sam Workdayton"]
    assert metrics.get("sources.workday.bad_record") == 1
    assert metrics.get("sources.workday.missing.email") == 1


def test_existing_signals_work_on_workday_data(tmp_path, db_path):
    ingest(db_path, "acme", workday_root(tmp_path))
    client = TestClient(create_app(db_path), token="tok-acme-reviewer")
    sam = client.get("/reviews/workday:JA-100234").json()
    assert [f["signal"] for f in sam["findings"]] == ["voip_phone"]
    assert len(sam["findings"][0]["evidence"]) == 1  # the re-delivered application added nothing
    assert sam["timeline"][0] == {**sam["timeline"][0], "source": "workday", "ts": "2026-09-14T17:22:00+00:00"}
    pat = client.get("/reviews/workday:JA-100235").json()  # no email at all, still reviewed
    assert [f["signal"] for f in pat["findings"]] == ["resume_name_mismatch"]
    assert client.get("/reviews/workday:JA-100236").json()["recommendation"] == "NONE"


def test_rerun_is_idempotent(tmp_path, db_path):
    root = workday_root(tmp_path)
    ingest(db_path, "acme", root)
    store = Store.open(db_path)
    again = Pipeline.for_tenant("acme", store).ingest(root)
    assert again.observations == 0 and again.identities == 4
    store.close()
