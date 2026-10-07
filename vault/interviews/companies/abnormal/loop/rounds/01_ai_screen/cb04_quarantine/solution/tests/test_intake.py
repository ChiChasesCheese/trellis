from __future__ import annotations

from datetime import datetime, timedelta, timezone

from quarantine.actions import drain
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


def test_reporter_gets_a_receipt_when_the_outbox_drains(app, make_payload):
    result = app.intake.submit("acme", make_payload())
    assert app.mailbox.receipts == []  # queued, not sent in the request
    assert drain(app.outbox, app.mailbox, "acme").delivered == 1
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
    drain(app.outbox, app.mailbox, "acme")
    assert [r["reporter"] for r in app.mailbox.receipts] == ["bob@acme.test", "carol@acme.test"]


def test_same_message_id_in_two_tenants_is_two_reports(app, make_payload):
    payload = make_payload()
    a = app.intake.submit("acme", payload)
    g = app.intake.submit("globex", payload)
    assert a.created and g.created
    assert a.report.id != g.report.id


def test_repeat_report_is_recorded_without_analysing_again(app, make_payload):
    from quarantine import metrics

    payload = make_payload(links=["https://files.docshare.example/d/1"])
    app.intake.submit("acme", payload)
    second = app.intake.submit("acme", {**payload, "reporter": "carol@acme.test"})
    assert second.report.reporter_count == 2
    assert metrics.total("analyzer.run") == 4


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


def test_the_same_reporter_twice_counts_once(app, make_payload):
    payload = make_payload()
    app.intake.submit("acme", payload)
    again = app.intake.submit("acme", payload)
    assert again.report.reporter_count == 1
    assert drain(app.outbox, app.mailbox, "acme").delivered == 1


def test_repeat_sender_window_is_measured_in_utc(app, make_payload):
    sender = {"From": "Promo <promo@bulk-unknown.example>"}
    for date in ("Mon, 14 Sep 2026 20:00:00 -0800", "Mon, 14 Sep 2026 21:00:00 -0800"):
        app.intake.submit("acme", make_payload(headers={**sender, "Date": date}))
    third = app.intake.submit("acme", make_payload(headers={**sender, "Date": "Tue, 15 Sep 2026 23:00:00 +0900"}))
    assert third.report.disposition is Disposition.QUARANTINE


def test_concurrent_reports_of_one_message_collapse(make_payload):
    import threading
    import time

    from quarantine.app import create_app
    from quarantine.config import FIXTURES_DIR
    from quarantine.lookups import FixtureUrlLookup

    inner = FixtureUrlLookup(FIXTURES_DIR / "intel" / "urls.json")

    class Slow:
        def check(self, url):
            time.sleep(0.1)
            return inner.check(url)

    app = create_app(url_lookup=Slow())
    payload = make_payload(links=["https://login-micros0ft.example/a"])
    barrier = threading.Barrier(4)
    results = []

    def go(i):
        barrier.wait()
        results.append(app.intake.submit("acme", {**payload, "reporter": f"u{i}@acme.test"}))

    threads = [threading.Thread(target=go, args=(i,)) for i in range(4)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert sum(r.created for r in results) == 1
    assert app.reports.count("acme") == 1
    assert len(app.mailbox.calls_of("quarantine")) == 1
    assert app.reports.find_by_message("acme", payload["message_id"]).reporter_count == 4


def test_analyzer_failure_sends_the_message_to_review(make_payload):
    from quarantine import metrics
    from quarantine.app import create_app

    class Broken:
        def check(self, url):
            raise RuntimeError("boom")

    app = create_app(url_lookup=Broken())
    result = app.intake.submit("acme", make_payload(links=["https://login-micros0ft.example/a"]))
    assert result.report.disposition is Disposition.NEEDS_REVIEW
    assert any(v.inconclusive for v in result.report.verdicts)
    assert metrics.get("analyzer.error", analyzer="link_reputation") == 1


def test_validation_errors(app, make_payload):
    import pytest

    from quarantine.errors import ValidationError

    for bad in (
        {"reporter": "bob@acme.test"},
        {"message_id": "<m>"},
        {"message_id": " ", "reporter": "bob@acme.test"},
        {"message_id": "<m>", "reporter": "bob@acme.test", "links": "http://x.example"},
        {"message_id": "<m>", "reporter": "bob@acme.test", "links": [1]},
        {"message_id": "<m>", "reporter": "bob@acme.test", "links": ["http://x.example"] * 51},
        {"message_id": "<m>", "reporter": "bob@acme.test", "attachments": [{"size": 1}]},
        {"message_id": "<m>", "reporter": "bob@acme.test", "headers": "From: x"},
    ):
        with pytest.raises(ValidationError):
            app.intake.submit("acme", bad)
    assert app.reports.count("acme") == 0


def test_logs_carry_ids_not_addresses(app, make_payload, caplog):
    import logging

    caplog.set_level(logging.DEBUG)
    app.intake.submit("acme", make_payload(reporter="pii.person@acme.test", links=["https://login-micros0ft.example/a"]))
    assert "pii.person@acme.test" not in caplog.text
