"""t2: Workday as a source. Reads the starter's own fixtures/workday; ingest via the CLI, read via the API."""
import json
import shutil
from datetime import datetime, timezone

import pytest
from vetting_helpers import RANK, World, signals


@pytest.fixture
def world(tmp_path):
    return World(tmp_path)


@pytest.fixture
def workday_root(tmp_path, codebase_root_path):
    root = tmp_path / "wd_only"
    shutil.copytree(codebase_root_path / "fixtures" / "workday", root / "workday")
    return root


@pytest.fixture
def ingested(world, workday_root):
    assert world.ingest("acme", workday_root) == 0
    return world


def find(world, name):
    return world.by_name("acme")[name]["identity_id"]


@pytest.mark.t2
@pytest.mark.core
def test_all_pages_are_ingested_and_the_redelivered_application_is_one_identity(ingested):
    names = sorted(ingested.by_name("acme"))
    assert names == ["Dana Cleanfield", "Lee Nophone", "Pat Noemailson", "Sam Workdayton"]


@pytest.mark.t2
@pytest.mark.core
def test_voip_number_with_split_country_code_and_extension_is_flagged(ingested):
    sam = ingested.review("acme", find(ingested, "Sam Workdayton"))
    assert "voip_phone" in signals(sam)
    assert sam["recommendation"] != "NONE"


@pytest.mark.t2
@pytest.mark.core
def test_the_timeline_names_workday_as_the_source(ingested):
    sam = ingested.review("acme", find(ingested, "Sam Workdayton"))
    assert sam["source"] == "workday"
    assert sam["timeline"][0]["source"] == "workday"
    assert "workday" in json.dumps(sam["timeline"]).lower()
    voip = next(f for f in sam["findings"] if f["signal"] == "voip_phone")
    assert all(c["source"] == "workday" for c in voip["evidence"])


@pytest.mark.t2
@pytest.mark.core
def test_a_redelivered_application_is_not_counted_twice(ingested):
    sam = ingested.review("acme", find(ingested, "Sam Workdayton"))
    voip = next(f for f in sam["findings"] if f["signal"] == "voip_phone")
    assert len(voip["evidence"]) == 1
    assert sum(1 for i in ingested.by_name("acme").values() if i["display_name"] == "Sam Workdayton") == 1


@pytest.mark.t2
@pytest.mark.core
def test_a_record_without_an_email_is_still_reviewed_on_its_other_signals(ingested):
    pat = ingested.review("acme", find(ingested, "Pat Noemailson"))
    assert "resume_name_mismatch" in signals(pat)
    assert pat["recommendation"] != "NONE"


@pytest.mark.t2
@pytest.mark.core
def test_offset_timestamps_are_converted_to_utc(ingested):
    sam = ingested.review("acme", find(ingested, "Sam Workdayton"))
    first = datetime.fromisoformat(sam["timeline"][0]["ts"])
    assert first == datetime(2026, 9, 14, 17, 22, tzinfo=timezone.utc)
    assert first.utcoffset().total_seconds() == 0


@pytest.mark.t2
@pytest.mark.stretch
def test_a_record_without_a_phone_survives_and_keeps_its_other_findings(ingested):
    lee = ingested.review("acme", find(ingested, "Lee Nophone"))
    assert "voip_phone" not in signals(lee) and "resume_name_mismatch" in signals(lee)
    assert ingested.review("acme", find(ingested, "Dana Cleanfield"))["recommendation"] == "NONE"


@pytest.mark.t2
@pytest.mark.stretch
def test_rerunning_the_ingest_is_idempotent(world, workday_root):
    assert world.ingest("acme", workday_root) == 0
    before = {n: (i["identity_id"], i["score"]) for n, i in world.by_name("acme").items()}
    assert world.ingest("acme", workday_root) == 0
    assert {n: (i["identity_id"], i["score"]) for n, i in world.by_name("acme").items()} == before
    assert len(before) == 4


@pytest.mark.t2
@pytest.mark.regression
def test_greenhouse_results_are_unchanged_when_both_sources_are_present(world, tmp_path, codebase_root_path):
    root = tmp_path / "both"
    shutil.copytree(codebase_root_path / "fixtures" / "greenhouse", root / "greenhouse")
    shutil.copytree(codebase_root_path / "fixtures" / "workday", root / "workday")
    assert world.ingest("acme", root) == 0
    jordan = world.review("acme", "greenhouse:40102")
    assert [f["signal"] for f in jordan["findings"]] == ["voip_phone"] and jordan["recommendation"] == "RECOMMENDED"
    kai = world.review("acme", "greenhouse:40120")
    assert signals(kai) == {"voip_phone", "ip_geo_mismatch", "resume_name_mismatch"}
    assert kai["recommendation"] == "HIGHLY_RECOMMENDED" and kai["timeline"][0]["source"] == "greenhouse"
    assert world.review("acme", "greenhouse:40105")["findings"] == []


@pytest.mark.t2
@pytest.mark.regression
def test_greenhouse_timeline_still_says_greenhouse(world, tmp_path, codebase_root_path):
    root = tmp_path / "gh"
    shutil.copytree(codebase_root_path / "fixtures" / "greenhouse", root / "greenhouse")
    assert world.ingest("acme", root) == 0
    first = world.review("acme", "greenhouse:40101")["timeline"][0]
    assert first["source"] == "greenhouse" and "Greenhouse" in first["text"]


@pytest.mark.t2
@pytest.mark.regression
def test_tenants_stay_isolated(world, workday_root):
    assert world.ingest("acme", workday_root) == 0
    assert world.client("globex").get("/reviews").json()["count"] == 0
