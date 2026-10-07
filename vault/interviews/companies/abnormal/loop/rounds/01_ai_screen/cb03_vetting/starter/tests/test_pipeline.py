import io

from vetting import scoring
from vetting.cli import main
from vetting.legacy.blocklist import is_blocked
from vetting.metrics import metrics
from vetting.models import Finding, Recommendation
from vetting.pipeline import Pipeline
from vetting.store import Store
from vetting.timeline import build_timeline

from conftest import FIXTURES


def reviews_by_name(db_path, tenant="acme"):
    store = Store.open(db_path)
    names = {i.id: i.display_name for i in store.identities.list(tenant)}
    out = {names[r.identity_id]: r for r in store.reviews.list(tenant)}
    store.close()
    return out


def test_ingest_fixtures_reviews_everyone(ingested):
    reviews = reviews_by_name(ingested)
    assert len(reviews) == 12
    assert reviews["Casey Fixture"].recommendation is Recommendation.NONE
    assert reviews["Jordan Placeholder"].recommendation is Recommendation.RECOMMENDED
    assert [f.signal for f in reviews["Jordan Placeholder"].findings] == ["voip_phone"]
    kai = reviews["Kai Mismatchwood"]
    assert kai.recommendation is Recommendation.HIGHLY_RECOMMENDED
    assert {f.signal for f in kai.findings} == {"voip_phone", "ip_geo_mismatch", "resume_name_mismatch"}


def test_diacritic_name_is_not_flagged_and_bystanders_sharing_an_ip_are_quiet(ingested):
    reviews = reviews_by_name(ingested)
    assert reviews["Zoë Testwood"].findings == []
    assert reviews["Avery Corporate"].findings == [] and reviews["Blake Corporate"].findings == []


def test_ingest_is_rerunnable_and_counts_orphans(db_path):
    metrics.reset()
    store = Store.open(db_path)
    pipeline = Pipeline.for_tenant("acme", store)
    first = pipeline.ingest(FIXTURES)
    second = pipeline.ingest(FIXTURES)
    assert second.observations == 0 and second.identities == first.identities
    assert metrics.get("pipeline.orphan_observations") > 0
    store.close()


def test_tenant_threshold_override_changes_the_tier(db_path):
    store = Store.open(db_path)
    Pipeline.for_tenant("globex", store).ingest(FIXTURES)
    kai = next(r for r in store.reviews.list("globex") if r.identity_id == "greenhouse:40120")
    assert kai.score == 75 and kai.recommendation is Recommendation.HIGHLY_RECOMMENDED
    store.close()


def test_scoring_caps_and_thresholds(settings):
    findings = [Finding("a", 60, "x"), Finding("b", 60, "y")]
    assert scoring.score(findings, settings) == (100, Recommendation.HIGHLY_RECOMMENDED)
    assert scoring.score([Finding("a", 20, "x")], settings)[1] is Recommendation.RECOMMENDED
    assert scoring.score([Finding("a", 19, "x")], settings)[1] is Recommendation.NONE


def test_timeline_is_chronological_and_every_entry_cites_a_source(ingested):
    store = Store.open(ingested)
    identity = store.identities.get("acme", "greenhouse:40120")
    review = store.reviews.get("acme", "greenhouse:40120")
    timeline = build_timeline(identity, store.observations.for_identity("acme", identity.id), review.findings)
    assert timeline[0].text == "Application received via Greenhouse"
    assert timeline[-1].text == "Detection complete"
    assert [e.ts for e in timeline[:-1]] == sorted(e.ts for e in timeline[:-1])
    assert all(e.source and e.ref for e in timeline)
    assert any(e.source == "idp" for e in timeline)
    store.close()


def test_cli_ingest_and_review(db_path):
    out = io.StringIO()
    assert main(["--db", str(db_path), "ingest", str(FIXTURES), "--tenant", "acme"], out) == 0
    assert "identities=12" in out.getvalue()
    out = io.StringIO()
    assert main(["--db", str(db_path), "review", "greenhouse:40120", "--tenant", "acme"], out) == 0
    assert "HIGHLY_RECOMMENDED" in out.getvalue() and "Detection complete" in out.getvalue()
    assert main(["--db", str(db_path), "review", "greenhouse:nope", "--tenant", "acme"], io.StringIO()) == 2


def test_legacy_blocklist_still_behaves():
    assert is_blocked(ip="203.0.113.66") and is_blocked(phone="+19005550100")
    assert not is_blocked(ip="203.0.113.20")
