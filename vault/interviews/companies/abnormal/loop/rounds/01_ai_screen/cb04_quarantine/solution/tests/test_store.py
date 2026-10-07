from __future__ import annotations

from datetime import datetime, timedelta, timezone

from quarantine.intake import parse_report
from quarantine.models import Disposition, ReportStatus, Verdict
from quarantine.store import ReportRepository, connect, migrate

NOW = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)


def _repo() -> ReportRepository:
    conn = connect()
    migrate(conn)
    return ReportRepository(conn)


def test_migrate_is_idempotent():
    conn = connect()
    assert migrate(conn) == ["0001_init", "0002_unique_report", "0003_outbox", "0004_reporters"]
    assert migrate(conn) == []


def test_insert_and_get_round_trip(make_payload):
    repo = _repo()
    report = parse_report(make_payload(links=["https://a.example"]), "acme", NOW)
    report.verdicts = [Verdict("link_reputation", 10, ("r",))]
    report.disposition, report.status = Disposition.RELEASE, ReportStatus.CLEARED
    repo.insert(report)
    loaded = repo.get("acme", report.id)
    assert loaded is not None
    assert loaded.to_dict() == report.to_dict()


def test_find_by_message_is_scoped_by_tenant(make_payload):
    repo = _repo()
    report = parse_report(make_payload(), "acme", NOW)
    repo.insert(report)
    assert repo.find_by_message("acme", report.message_id).id == report.id
    assert repo.find_by_message("globex", report.message_id) is None


def test_list_is_newest_first_and_paged(make_payload):
    repo = _repo()
    ids = []
    for i in range(5):
        r = parse_report(make_payload(), "acme", NOW + timedelta(minutes=i))
        repo.insert(r)
        ids.append(r.id)
    page = repo.list("acme", limit=2, offset=1)
    assert [r.id for r in page] == [ids[3], ids[2]]
    assert repo.count("acme") == 5
    assert repo.list("globex") == []


def test_count_sender_reports_window(make_payload):
    repo = _repo()
    for hour in (6, 7, 8):
        r = parse_report(
            make_payload(headers={"From": "s@x.example", "Date": f"Tue, 15 Sep 2026 0{hour}:00:00 +0000"}),
            "acme",
            NOW,
        )
        repo.insert(r)
    since = datetime(2026, 9, 15, 6, 30, tzinfo=timezone.utc)
    until = datetime(2026, 9, 15, 9, 0, tzinfo=timezone.utc)
    assert repo.count_sender_reports("acme", "s@x.example", since, until, "<none>") == 2
    assert repo.count_sender_reports("globex", "s@x.example", since, until, "<none>") == 0


def test_get_is_scoped_by_tenant(make_payload):
    repo = _repo()
    report = parse_report(make_payload(), "acme", NOW)
    repo.insert(report)
    assert repo.get("globex", report.id) is None
    assert repo.get("acme", report.id) is not None


def test_second_report_of_a_message_is_a_duplicate(make_payload):
    import pytest

    from quarantine.errors import DuplicateReport

    repo = _repo()
    payload = make_payload()
    repo.insert(parse_report(payload, "acme", NOW))
    with pytest.raises(DuplicateReport):
        repo.insert(parse_report(payload, "acme", NOW))
    repo.insert(parse_report(payload, "globex", NOW))  # another tenant may file the same message id


def test_reporters_are_counted_once_each(make_payload):
    repo = _repo()
    report = parse_report(make_payload(), "acme", NOW)
    repo.insert(report)
    assert repo.add_reporter("acme", report.id, "carol@acme.test", NOW) is True
    assert repo.add_reporter("acme", report.id, "carol@acme.test", NOW) is False
    assert repo.add_reporter("acme", report.id, report.reporter, NOW) is False
    assert repo.reporter_count("acme", report.id) == 2
    assert repo.get("acme", report.id).reporter_count == 2


def test_set_status_if_only_moves_from_the_expected_states(make_payload):
    repo = _repo()
    report = parse_report(make_payload(), "acme", NOW)
    report.status = ReportStatus.CLEARED
    repo.insert(report)
    assert not repo.set_status_if("acme", report.id, (ReportStatus.QUARANTINED,), ReportStatus.RELEASED)
    assert repo.set_status_if("acme", report.id, (ReportStatus.CLEARED,), ReportStatus.RELEASED)
