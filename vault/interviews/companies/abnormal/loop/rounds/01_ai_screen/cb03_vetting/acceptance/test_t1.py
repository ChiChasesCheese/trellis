"""t1: surface coordinated applicants. Only the CLI ingest and GET /reviews are used."""
import json

import pytest
from vetting_helpers import RANK, World, findings_text, gh_record

A, B, C = "greenhouse:101", "greenhouse:102", "greenhouse:103"
SHA = "a" * 64
FACTORY = dict(author="Resume Factory", tool="ExamplePDF Engine 3.1")


def campaign():
    """Three different names; shared phone block (three formats), shared /24, shared resume fingerprint."""
    return [
        gh_record(101, "Taylor", "Exampleton", "(415) 555-0143", "198.51.100.21", digest=SHA, **FACTORY),
        gh_record(102, "Jamie", "Samplesmith", "415.555.0147", "198.51.100.22", digest=SHA, **FACTORY),
        gh_record(103, "Robin", "Testovich", "+1-415-555-0152 ext. 9", "198.51.100.37", **FACTORY),
    ]


def bystanders():
    """Two ordinary people whose only overlap is one shared office NAT address."""
    return [
        gh_record(201, "Avery", "Corporate", "(206) 555-0106", "192.0.2.70"),
        gh_record(202, "Blake", "Corporate", "(503) 555-0107", "192.0.2.70"),
    ]


@pytest.fixture
def world(tmp_path):
    return World(tmp_path)


@pytest.mark.t1
@pytest.mark.core
def test_campaign_members_are_raised(world):
    world.ingest_records("acme", campaign())
    for member in (A, B, C):
        assert world.level("acme", member) >= RANK["RECOMMENDED"], member


@pytest.mark.t1
@pytest.mark.core
def test_each_member_shows_the_other_two_in_its_findings(world):
    world.ingest_records("acme", campaign())
    for member in (A, B, C):
        text = findings_text(world.review("acme", member))
        for other in {A, B, C} - {member}:
            assert other in text, f"{member} has no evidence pointing at {other}"


@pytest.mark.t1
@pytest.mark.core
def test_correlation_evidence_is_cited_like_every_other_finding(world):
    world.ingest_records("acme", campaign())
    findings = world.review("acme", A)["findings"]
    linking = [f for f in findings if B in json.dumps(f)]
    assert linking, "no finding mentions the other applicants"
    for finding in linking:
        assert finding["weight"] > 0 and finding["summary"]
        assert finding["evidence"], "a finding without citations"
        for citation in finding["evidence"]:
            assert citation["source"] and citation["ref"] and citation["ts"]


@pytest.mark.t1
@pytest.mark.core
def test_a_shared_office_ip_alone_does_not_condemn_anyone(world):
    world.ingest_records("acme", campaign() + bystanders())
    assert world.level("acme", A) >= RANK["RECOMMENDED"]  # the campaign is still found
    for ident in ("greenhouse:201", "greenhouse:202"):
        assert world.level("acme", ident) == RANK["NONE"], ident


@pytest.mark.t1
@pytest.mark.core
def test_phone_formats_and_neighbouring_ips_are_normalized(world):
    world.ingest_records("acme", [
        gh_record(301, "Ann", "Alpha", "(206) 555-0101", "198.51.100.40"),
        gh_record(302, "Bob", "Beta", "+1 206-555-0101 x12", "198.51.100.41"),
    ])
    assert world.level("acme", "greenhouse:301") >= RANK["RECOMMENDED"]
    assert "greenhouse:302" in findings_text(world.review("acme", "greenhouse:301"))


@pytest.mark.t1
@pytest.mark.core
def test_members_ingested_in_separate_runs_all_end_up_linked(world):
    members = campaign()
    for record in members:
        world.ingest_records("acme", [record])
    for member in (A, B, C):
        text = findings_text(world.review("acme", member))
        assert all(other in text for other in {A, B, C} - {member}), member


@pytest.mark.t1
@pytest.mark.core
def test_tier_filter_lists_the_members(world):
    world.ingest_records("acme", campaign() + bystanders())
    client = world.client("acme")
    flagged = {
        item["identity_id"]
        for tier in ("RECOMMENDED", "HIGHLY_RECOMMENDED")
        for item in client.get("/reviews", recommendation=tier).json()["items"]
    }
    assert {A, B, C} <= flagged
    assert not flagged & {"greenhouse:201", "greenhouse:202"}


@pytest.mark.t1
@pytest.mark.stretch
def test_the_timeline_cites_the_other_applicants(world):
    world.ingest_records("acme", campaign())
    timeline = json.dumps(world.review("acme", A)["timeline"])
    assert B in timeline and C in timeline


@pytest.mark.t1
@pytest.mark.stretch
def test_common_values_do_not_link_unrelated_people_but_a_five_member_campaign_is_complete(world):
    members = campaign() + [
        gh_record(104, "Quinn", "Fourth", "(415) 555-0161", "198.51.100.50", **FACTORY),
        gh_record(105, "Sky", "Fifth", "(415) 555-0170", "198.51.100.51", **FACTORY),
    ]
    decoys = [  # same user agent, same resume tool, same /24 of a big residential ISP: nothing else
        gh_record(401 + i, f"Decoy{n}", "Person", f"({200 + i * 7}) 555-01{i:02d}", f"192.0.2.{10 + i}")
        for i, n in enumerate(["Aa", "Bb", "Cc", "Dd"])
    ]
    world.ingest_records("acme", members + decoys)
    ids = [f"greenhouse:{r['id']}" for r in members]
    for me in ids:
        text = findings_text(world.review("acme", me))
        assert all(other in text for other in ids if other != me), me
    for i in range(4):
        assert world.level("acme", f"greenhouse:{401 + i}") == RANK["NONE"]


@pytest.mark.t1
@pytest.mark.regression
def test_existing_signals_still_fire_and_clean_people_stay_clean(world):
    world.ingest_records("acme", [
        gh_record(501, "Jordan", "Placeholder", "+1 (646) 555-0102", "192.0.2.12"),
        gh_record(502, "Casey", "Fixture", "(212) 555-0101", "192.0.2.10"),
    ])
    voip = world.review("acme", "greenhouse:501")
    assert [f["signal"] for f in voip["findings"]] == ["voip_phone"] and voip["recommendation"] == "RECOMMENDED"
    assert world.review("acme", "greenhouse:502")["findings"] == []


@pytest.mark.t1
@pytest.mark.regression
def test_a_shared_office_ip_alone_is_quiet(world):
    world.ingest_records("acme", bystanders())
    assert world.level("acme", "greenhouse:201") == world.level("acme", "greenhouse:202") == RANK["NONE"]


@pytest.mark.t1
@pytest.mark.regression
def test_the_same_numbers_in_another_tenant_are_not_correlated(world):
    one, two = campaign()[:2]
    world.ingest_records("acme", [one])
    world.ingest_records("globex", [two])
    assert world.level("acme", A) == RANK["NONE"]
    assert world.level("globex", B) == RANK["NONE"]


@pytest.mark.t1
@pytest.mark.regression
def test_reingesting_the_same_files_changes_nothing(world):
    root = world.batch(campaign() + bystanders())
    assert world.ingest("acme", root) == 0
    before = {n: (i["recommendation"], i["score"]) for n, i in world.by_name("acme").items()}
    assert world.ingest("acme", root) == 0
    assert {n: (i["recommendation"], i["score"]) for n, i in world.by_name("acme").items()} == before
    assert len(before) == 5
