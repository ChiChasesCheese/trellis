from vetting.metrics import metrics
from vetting.models import Kind
from vetting.sources import SOURCES
from vetting.sources.greenhouse import GreenhouseSource
from vetting.sources.idp import IdpSource

from conftest import FIXTURES, write_json


def test_registry_has_the_two_sources():
    assert set(SOURCES) == {"greenhouse", "idp"}


def test_greenhouse_maps_a_record_to_identity_and_observations():
    metrics.reset()
    batches = list(GreenhouseSource().load(FIXTURES, "acme"))
    by_id = {b.identity.id: b for b in batches}
    kai = by_id["greenhouse:40120"]
    assert kai.identity.display_name == "Kai Mismatchwood" and kai.identity.tenant_id == "acme"
    kinds = {o.kind for o in kai.observations}
    assert {Kind.NAME, Kind.EMAIL, Kind.PHONE, Kind.IP, Kind.RESUME_SHA256, Kind.RESUME_NAME} <= kinds
    phone = next(o for o in kai.observations if o.kind is Kind.PHONE)
    assert phone.value == "929-555-0120" and phone.raw_ref == "greenhouse:40120#candidate.phone_numbers[0]"
    assert phone.ts.utcoffset().total_seconds() == 0


def test_greenhouse_counts_and_skips_bad_records_but_keeps_the_good_one():
    metrics.reset()
    ids = [b.identity.id for b in GreenhouseSource().load(FIXTURES, "acme")]
    assert "greenhouse:40130" in ids and "greenhouse:40131" not in ids
    assert metrics.get("sources.greenhouse.bad_record") == 3


def test_missing_optional_field_skips_only_that_observation(tmp_path):
    metrics.reset()
    record = {"id": 1, "applied_at": "2026-09-01T00:00:00Z", "candidate": {"first_name": "A", "last_name": "B"}}
    write_json(tmp_path / "greenhouse/applications/x.json", [record])
    (batch,) = GreenhouseSource().load(tmp_path, "acme")
    assert {o.kind for o in batch.observations} == {Kind.NAME}
    assert metrics.get("sources.greenhouse.missing.email") == 1


def test_idp_events_carry_no_identity_and_bad_lines_are_counted():
    metrics.reset()
    batches = list(IdpSource().load(FIXTURES, "acme"))
    assert len(batches) == 4 and all(b.identity is None for b in batches)
    assert metrics.get("sources.idp.bad_record") == 1
    assert {o.kind for o in batches[0].observations} == {Kind.LOGIN_IP, Kind.LOGIN_COUNTRY, Kind.DEVICE}
