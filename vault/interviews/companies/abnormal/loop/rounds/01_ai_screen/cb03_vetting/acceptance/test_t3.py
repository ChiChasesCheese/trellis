"""t3: use reviewer decisions. POST /reviews/<id>/disposition is the only way a decision is made."""
import pytest
from vetting_helpers import RANK, World, findings_text, gh_record, signals

ASN_ONE = ("203.0.113.31", "203.0.113.32", "203.0.113.33")  # ExampleVPN, AS64500
ASN_TWO = "203.0.113.140"  # OtherExampleVPN, AS64501


@pytest.fixture
def world(tmp_path):
    return World(tmp_path)


def a(): return gh_record(601, "Ann", "Alpha", "(206) 555-0101", ASN_ONE[0])  # lone VPN signal
def b(): return gh_record(602, "Bob", "Beta", "(312) 555-0102", ASN_ONE[1])  # lone VPN signal, same ASN
def d(): return gh_record(604, "Dee", "Delta", "(404) 555-0104", ASN_TWO)  # lone VPN signal, other ASN
def strong():  # VoIP + name mismatch + same VPN ASN
    return gh_record(603, "Cy", "Gamma", "+1 646 555 0102", ASN_ONE[2], resume_name="Cye Gammon")


def control(world, record, ident):
    """The level the same applicant gets in a tenant where nobody has decided anything."""
    world.ingest_records("globex", [record])
    return world.level("globex", ident)


@pytest.mark.t3
@pytest.mark.core
def test_a_cleared_vpn_network_softens_the_next_lone_vpn_applicant(world):
    world.ingest_records("acme", [a()])
    world.decide("acme", "greenhouse:601", "cleared", "corporate VPN")
    world.ingest_records("acme", [b()])
    assert control(world, b(), "greenhouse:602") == RANK["RECOMMENDED"]
    assert world.level("acme", "greenhouse:602") < RANK["RECOMMENDED"]


@pytest.mark.t3
@pytest.mark.core
def test_the_evidence_is_kept_and_marked_as_previously_cleared(world):
    world.ingest_records("acme", [a()])
    world.decide("acme", "greenhouse:601", "cleared")
    world.ingest_records("acme", [b()])
    detail = world.review("acme", "greenhouse:602")
    assert world.level("acme", "greenhouse:602") == RANK["NONE"]
    vpn = [f for f in detail["findings"] if f["signal"] == "vpn_hosting_ip"]
    assert vpn and vpn[0]["evidence"], "the finding must stay, with its citations"
    assert "cleared" in findings_text(detail).lower()


@pytest.mark.t3
@pytest.mark.core
def test_a_strong_combination_is_not_softened(world):
    world.ingest_records("acme", [a()])
    world.decide("acme", "greenhouse:601", "cleared")
    world.ingest_records("acme", [b(), strong()])
    assert world.level("acme", "greenhouse:602") < RANK["RECOMMENDED"]  # the lone one is softened ...
    assert world.review("acme", "greenhouse:603")["recommendation"] == "HIGHLY_RECOMMENDED"  # ... this one is not
    assert {"vpn_hosting_ip", "voip_phone", "resume_name_mismatch"} <= signals(world.review("acme", "greenhouse:603"))


@pytest.mark.t3
@pytest.mark.core
def test_only_the_cleared_value_is_softened_not_the_whole_signal(world):
    world.ingest_records("acme", [a()])
    world.decide("acme", "greenhouse:601", "cleared")
    world.ingest_records("acme", [b(), d()])
    assert world.level("acme", "greenhouse:602") < RANK["RECOMMENDED"]  # same ASN as the cleared one
    assert world.level("acme", "greenhouse:604") == RANK["RECOMMENDED"]  # a different VPN network


@pytest.mark.t3
@pytest.mark.core
def test_the_decision_keeps_applying_when_everything_is_ingested_again(world):
    world.ingest_records("acme", [a()])
    world.decide("acme", "greenhouse:601", "cleared")
    root = world.batch([b()])
    assert world.ingest("acme", root) == 0 and world.ingest("acme", root) == 0
    assert world.level("acme", "greenhouse:602") < RANK["RECOMMENDED"]


@pytest.mark.t3
@pytest.mark.stretch
def test_an_escalated_value_is_never_softened(world):
    world.ingest_records("acme", [
        a(),
        gh_record(605, "Eve", "Epsilon", "(770) 555-0105", ASN_ONE[2]),
        gh_record(606, "Fay", "Zeta", "(678) 555-0106", "203.0.113.141"),
    ])
    world.decide("acme", "greenhouse:601", "cleared")
    world.decide("acme", "greenhouse:605", "escalated", "operator network")
    world.decide("acme", "greenhouse:606", "cleared")  # a different network that nobody escalated
    world.ingest_records("acme", [b(), d()])
    assert world.level("acme", "greenhouse:602") == RANK["RECOMMENDED"]  # AS64500: cleared once, escalated once
    assert world.level("acme", "greenhouse:604") < RANK["RECOMMENDED"]  # AS64501: only cleared


@pytest.mark.t3
@pytest.mark.stretch
def test_a_cleared_number_softens_a_lone_voip_reapplication_in_another_format(world):
    world.ingest_records("acme", [gh_record(611, "Pia", "Voice", "(646) 555-0102", "192.0.2.12")])
    assert world.level("acme", "greenhouse:611") == RANK["RECOMMENDED"]
    world.decide("acme", "greenhouse:611", "cleared", "legitimate Google Voice user")
    world.ingest_records("acme", [gh_record(612, "Pia", "Revoice", "+1 646 555 0102 x4", "198.51.100.77")])
    assert world.level("acme", "greenhouse:612") < RANK["RECOMMENDED"]


@pytest.mark.t3
@pytest.mark.regression
def test_without_any_decision_a_lone_vpn_applicant_is_still_recommended(world):
    world.ingest_records("acme", [a(), b()])
    for ident in ("greenhouse:601", "greenhouse:602"):
        review = world.review("acme", ident)
        assert review["recommendation"] == "RECOMMENDED" and signals(review) == {"vpn_hosting_ip"}
        assert review["score"] == 20


@pytest.mark.t3
@pytest.mark.regression
def test_the_disposition_history_stays_queryable(world):
    world.ingest_records("acme", [a()])
    world.decide("acme", "greenhouse:601", "escalated", "first look")
    world.decide("acme", "greenhouse:601", "cleared", "verified with manager")
    detail = world.review("acme", "greenhouse:601")
    assert detail["disposition"] == "cleared"
    assert [(x["decision"], x["note"]) for x in detail["dispositions"]] == [
        ("escalated", "first look"),
        ("cleared", "verified with manager"),
    ]


@pytest.mark.t3
@pytest.mark.regression
def test_a_decision_in_another_tenant_changes_nothing_here(world):
    world.ingest_records("globex", [a()])
    world.decide("globex", "greenhouse:601", "cleared")
    world.ingest_records("acme", [b()])
    assert world.level("acme", "greenhouse:602") == RANK["RECOMMENDED"]
