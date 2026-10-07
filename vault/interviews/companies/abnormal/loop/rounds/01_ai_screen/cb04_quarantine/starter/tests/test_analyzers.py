from __future__ import annotations

from datetime import datetime, timezone

from quarantine.analyzers import ANALYZERS, AnalysisContext, AnalyzerRunner
from quarantine.config import FIXTURES_DIR, SettingsProvider
from quarantine.decision import decide
from quarantine.intake import parse_report
from quarantine.lookups import FixtureUrlLookup, SenderIntel
from quarantine.models import Disposition, Verdict
from quarantine.config import DecisionSettings
from quarantine.store import ReportRepository, connect, migrate

NOW = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)


def _ctx() -> AnalysisContext:
    conn = connect()
    migrate(conn)
    return AnalysisContext(
        settings=SettingsProvider(),
        reports=ReportRepository(conn),
        url_lookup=FixtureUrlLookup(FIXTURES_DIR / "intel" / "urls.json"),
        sender_intel=SenderIntel(FIXTURES_DIR / "intel" / "senders.json"),
    )


def _run(name: str, payload: dict, tenant: str = "acme") -> Verdict:
    return ANALYZERS[name]().analyze(parse_report(payload, tenant, NOW), _ctx())


def test_registry_has_the_four_analyzers():
    assert sorted(ANALYZERS) == [
        "attachment_type", "display_name_spoof", "link_reputation", "sender_reputation",
    ]


def test_sender_known_domain_uses_intel(make_payload):
    v = _run("sender_reputation", make_payload(headers={"From": "x@payroll-update.example"}))
    assert v.score == 85


def test_sender_unknown_domain_uses_default(make_payload):
    v = _run("sender_reputation", make_payload(headers={"From": "x@never-seen.example"}))
    assert v.score == 30


def test_link_reputation_takes_the_worst_link(make_payload):
    v = _run("link_reputation", make_payload(links=["https://docs.partner.example/a", "https://login-micros0ft.example/b"]))
    assert v.score == 95
    assert "phishing" in v.reasons[0]


def test_link_reputation_unknown_host_is_clean(make_payload):
    assert _run("link_reputation", make_payload(links=["https://example.org/"])).score == 0


def test_attachment_double_extension(make_payload):
    v = _run("attachment_type", make_payload(attachments=[{"filename": "scan.pdf.exe"}]))
    assert v.score == 95


def test_attachment_risky_extension_and_archive(make_payload):
    assert _run("attachment_type", make_payload(attachments=[{"filename": "macro.docm"}])).score == 75
    assert _run("attachment_type", make_payload(attachments=[{"filename": "files.zip"}])).score == 40
    assert _run("attachment_type", make_payload(attachments=[{"filename": "notes.pdf"}])).score == 0


def test_display_name_spoof_needs_outside_domain(make_payload):
    spoof = make_payload(headers={"From": '"Alice Chen" <ceo@freemail.example>'})
    assert _run("display_name_spoof", spoof).score == 80
    genuine = make_payload(headers={"From": '"Alice Chen" <alice@acme.test>'})
    assert _run("display_name_spoof", genuine).score == 0


def test_display_name_protected_list_is_per_tenant(make_payload):
    payload = make_payload(headers={"From": '"Dana Whitfield" <d@freemail.example>'})
    assert _run("display_name_spoof", payload, "acme").score == 0
    assert _run("display_name_spoof", payload, "globex").score == 80


def test_runner_counts_every_analyzer_run(make_payload):
    from quarantine import metrics

    report = parse_report(make_payload(), "acme", NOW)
    verdicts = AnalyzerRunner(_ctx()).run(report)
    assert len(verdicts) == 4
    assert metrics.total("analyzer.run") == 4
    assert metrics.get("analyzer.run", analyzer="link_reputation") == 1


def test_decide_thresholds():
    s = DecisionSettings(quarantine_at=70, review_at=40)
    assert decide([Verdict("a", 10), Verdict("b", 39)], s) is Disposition.RELEASE
    assert decide([Verdict("a", 40)], s) is Disposition.NEEDS_REVIEW
    assert decide([Verdict("a", 20), Verdict("b", 70)], s) is Disposition.QUARANTINE
    assert decide([], s) is Disposition.RELEASE


def test_tenant_threshold_changes_the_outcome(app, make_payload):
    payload = make_payload(headers={"From": "x@gmail-support.example"})  # sender risk 60
    assert app.intake.submit("acme", payload).report.disposition is Disposition.NEEDS_REVIEW
    other = make_payload(headers={"From": "x@gmail-support.example"})
    assert app.intake.submit("globex", other).report.disposition is Disposition.QUARANTINE
