from __future__ import annotations

from datetime import datetime, timedelta, timezone

from quarantine.intake import parse_report
from quarantine.models import Disposition, ReportStatus

NOW = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)


def test_parse_report_extracts_sender_and_display_name(make_payload):
    payload = make_payload(headers={"From": '"Alice Chen" <Alice.Chen@Gmail-Support.example>'})
    report = parse_report(payload, "acme", NOW)
    assert report.sender == "alice.chen@gmail-support.example"
    assert report.display_name == "Alice Chen"
    assert report.tenant_id == "acme"
    assert report.id.startswith("rpt_")


def test_parse_report_reads_links_and_attachments(make_payload):
    payload = make_payload(
        links=["https://a.example/x"],
        attachments=[{"filename": "a.zip", "size": 10}],
    )
    report = parse_report(payload, "acme", NOW)
    assert report.links == ["https://a.example/x"]
    assert report.attachments[0].filename == "a.zip"
    assert report.attachments[0].content_type == "application/octet-stream"


def test_missing_date_header_falls_back_to_received_time(make_payload):
    payload = make_payload()
    del payload["headers"]["Date"]
    report = parse_report(payload, "acme", NOW)
    assert report.sent_at.replace(tzinfo=timezone.utc) == NOW


def test_submit_clean_message_is_cleared(app, make_payload):
    result = app.intake.submit("acme", make_payload())
    assert result.created
    assert result.report.disposition is Disposition.RELEASE
    assert result.report.status is ReportStatus.CLEARED
    assert app.mailbox.calls_of("quarantine") == []


def test_submit_bad_link_is_quarantined(app, make_payload):
    result = app.intake.submit("acme", make_payload(links=["https://login-micros0ft.example/a"]))
    assert result.report.disposition is Disposition.QUARANTINE
    assert result.report.status is ReportStatus.QUARANTINED
    assert app.mailbox.calls == [("quarantine", "acme", result.report.message_id)]


def test_reporter_gets_a_receipt(app, make_payload):
    result = app.intake.submit("acme", make_payload())
    assert app.mailbox.receipts == [
        {
            "tenant_id": "acme",
            "reporter": "bob@acme.test",
            "report_id": result.report.id,
            "disposition": "RELEASE",
        }
    ]


def test_same_message_reported_twice_is_one_report(app, make_payload):
    payload = make_payload(links=["https://login-micros0ft.example/a"])
    first = app.intake.submit("acme", payload)
    second = app.intake.submit("acme", {**payload, "reporter": "carol@acme.test"})
    assert first.created and not second.created
    assert second.report.id == first.report.id
    assert app.reports.count("acme") == 1
    assert len(app.mailbox.calls_of("quarantine")) == 1
    assert [r["reporter"] for r in app.mailbox.receipts] == ["bob@acme.test", "carol@acme.test"]


def test_same_message_id_in_two_tenants_is_two_reports(app, make_payload):
    payload = make_payload()
    a = app.intake.submit("acme", payload)
    g = app.intake.submit("globex", payload)
    assert a.created and g.created
    assert a.report.id != g.report.id


def test_repeat_report_reevaluates_with_current_intel(app, make_payload):
    payload = make_payload(links=["https://files.docshare.example/d/1"])
    first = app.intake.submit("acme", payload)
    assert first.report.disposition is Disposition.NEEDS_REVIEW
    second = app.intake.submit("acme", {**payload, "reporter": "carol@acme.test"})
    assert second.report.disposition is Disposition.NEEDS_REVIEW
    assert metrics_total("analyzer.run") == 8


def metrics_total(name: str) -> int:
    from quarantine import metrics

    return metrics.total(name)


def test_sender_repeated_within_window_raises_score(app, make_payload):
    sender = {"From": "Promo <promo@bulk-unknown.example>"}
    first = app.intake.submit("acme", make_payload(headers=sender))
    second = app.intake.submit("acme", make_payload(headers={**sender, "Date": "Tue, 15 Sep 2026 09:00:00 +0000"}))
    third = app.intake.submit("acme", make_payload(headers={**sender, "Date": "Tue, 15 Sep 2026 10:00:00 +0000"}))
    assert first.report.disposition is Disposition.RELEASE
    assert second.report.disposition is Disposition.NEEDS_REVIEW
    assert third.report.disposition is Disposition.QUARANTINE


def test_sender_reports_outside_window_do_not_count(app, make_payload):
    sender = {"From": "Promo <promo@bulk-unknown.example>"}
    app.intake.submit("acme", make_payload(headers={**sender, "Date": "Sat, 12 Sep 2026 08:00:00 +0000"}))
    later = app.intake.submit("acme", make_payload(headers=sender))
    assert later.report.disposition is Disposition.RELEASE


def test_received_time_is_the_injected_clock(app, make_payload):
    result = app.intake.submit("acme", make_payload())
    assert result.report.received_at == NOW
    assert NOW - result.report.sent_at.replace(tzinfo=timezone.utc) == timedelta(hours=4)
