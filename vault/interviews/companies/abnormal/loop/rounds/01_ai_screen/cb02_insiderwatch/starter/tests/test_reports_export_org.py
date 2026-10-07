import csv
import io
import json
from datetime import datetime, timedelta, timezone

import pytest

from insiderwatch.alerts import Alert
from insiderwatch.check import check_raw_dir, unregistered_sources
from insiderwatch.cli import main
from insiderwatch.errors import InsiderWatchError
from insiderwatch.events import Action, Event, email_domain, is_external
from insiderwatch.export import export_alerts
from insiderwatch.hr import Employee, Roster
from insiderwatch.hr.org import direct_reports, manager_chain
from insiderwatch.report import render_risk_table, risk_table

NOW = datetime(2026, 9, 30, 12, tzinfo=timezone.utc)


def alert(user, score, days_ago=0, signal="volume_spike"):
    return Alert(user=user, signal=signal, score=score, ts=NOW - timedelta(days=days_ago), reasons=["a", "b"])


def test_risk_table_ranks_by_decayed_risk(config):
    rows = risk_table([alert("old@x", 0.9, 60), alert("new@x", 0.3, 0), alert("new@x", 0.3, 1, "off_hours_activity")],
                      NOW, config)
    assert [r.user for r in rows] == ["new@x", "old@x"]
    assert rows[0].alert_count == 2 and rows[0].severity == "low"
    assert "new@x" in render_risk_table(rows)


def test_export_formats(config):
    alerts = [alert("a@x", 0.8)]
    assert json.loads(export_alerts(alerts, "jsonl", config))["severity"] == "high"
    parsed = list(csv.DictReader(io.StringIO(export_alerts(alerts, "csv", config))))
    assert parsed[0]["reasons"] == "a | b"
    with pytest.raises(InsiderWatchError):
        export_alerts(alerts, "xml", config)


def test_manager_chain_and_reports_handle_cycles():
    roster = Roster([Employee("a@x", "A", "d", manager="b@x"), Employee("b@x", "B", "d", manager="c@x"),
                     Employee("c@x", "C", "d", manager="a@x")])
    assert [e.email for e in manager_chain(roster, "a@x")] == ["b@x", "c@x"]
    assert [e.email for e in direct_reports(roster, "b@x")] == ["a@x"]
    assert manager_chain(roster, "ghost@x") == []


def test_event_requires_aware_timestamp_and_normalizes_user():
    with pytest.raises(ValueError):
        Event("a@x", datetime(2026, 9, 1), Action.LOGIN)
    ev = Event(" A@X ", datetime(2026, 9, 1, tzinfo=timezone.utc), Action.LOGIN)
    assert ev.user == "a@x" and ev.day.isoformat() == "2026-09-01"


def test_external_address_helpers():
    assert email_domain("Bob@Gmail.com") == "gmail.com"
    assert is_external("bob@gmail.com", ["acme.example"]) and not is_external("bob@ACME.example", ["acme.example"])
    assert not is_external("not-an-address", ["acme.example"])


def test_check_reports_sources_and_unclaimed_dirs(fixtures_dir, config):
    report = check_raw_dir(fixtures_dir / "raw", config)
    assert report["okta"]["emitted"] > 0 and report["okta"]["users"] >= 8
    assert "gdrive" in unregistered_sources(fixtures_dir / "raw", config) or "gdrive" in report


def test_cli_risk_export_check(tmp_path, capsys, fixtures_dir):
    db = str(tmp_path / "iw.db")
    assert main(["--db", db, "replay", str(fixtures_dir / "raw"), "--until", "2026-09-30"]) == 0
    capsys.readouterr()
    assert main(["--db", db, "risk", "--as-of", "2026-09-30"]) == 0
    assert "henry.ross@acme.example" in capsys.readouterr().out
    assert main(["--db", db, "export", "--format", "csv"]) == 0
    assert capsys.readouterr().out.splitlines()[0].startswith("id,ts,user")
    assert main(["check", str(fixtures_dir / "raw")]) == 0
