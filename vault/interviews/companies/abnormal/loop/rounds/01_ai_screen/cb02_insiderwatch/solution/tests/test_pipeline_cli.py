import json
import subprocess
import sys
from pathlib import Path

import pytest

from insiderwatch.cli import main
from insiderwatch.db import migrate, open_db

ROOT = Path(__file__).resolve().parent.parent


def run_cli(capsys, *argv):
    code = main([str(a) for a in argv])
    out = capsys.readouterr()
    return code, out.out, out.err


@pytest.fixture(scope="module")
def replayed(tmp_path_factory):
    """One replay of the whole fixture set, shared by the read-only assertions below."""
    db = tmp_path_factory.mktemp("replay") / "iw.db"
    proc = subprocess.run(
        [sys.executable, "-m", "insiderwatch", "--db", str(db), "replay", "fixtures/raw", "--until", "2026-09-30", "--json"],
        cwd=ROOT, capture_output=True, text=True, check=True)
    return db, json.loads(proc.stdout)


def test_replay_summary_counts(replayed):
    _, summary = replayed
    assert summary["by_source"].keys() >= {"m365_audit", "okta", "slack_audit"}
    assert summary["events"] == sum(summary["by_source"].values()) == sum(summary["by_action"].values())
    assert summary["dropped"]["m365_audit"] > 0


def test_existing_signals_alert_on_fixture_users(replayed, capsys):
    db, _ = replayed
    code, out, _ = run_cli(capsys, "--db", db, "alerts", "--user", "alice.nguyen@acme.example", "--json")
    signals = {a["signal"] for a in json.loads(out)}
    assert code == 0 and signals == {"volume_spike", "off_hours_activity", "unusual_login_location"}


def test_quiet_users_have_no_alerts(replayed, capsys):
    db, _ = replayed
    _, out, _ = run_cli(capsys, "--db", db, "alerts", "--json")
    users = {a["user"] for a in json.loads(out)}
    assert not users & {"bob.martin@acme.example", "dave.kim@acme.example", "frank.okafor@acme.example"}


def test_alerts_json_carries_severity(replayed, capsys):
    db, _ = replayed
    _, out, _ = run_cli(capsys, "--db", db, "alerts", "--json")
    assert {a["severity"] for a in json.loads(out)} <= {"low", "medium", "high"}


def test_replay_is_incremental_and_idempotent(tmp_path, capsys):
    db = tmp_path / "iw.db"
    raw = ROOT / "fixtures" / "raw"
    run_cli(capsys, "--db", db, "replay", raw, "--until", "2026-09-05")
    _, first, _ = run_cli(capsys, "--db", db, "alerts", "--json")
    code, out, _ = run_cli(capsys, "--db", db, "replay", raw, "--until", "2026-09-05", "--json")
    assert code == 0 and json.loads(out)["events"] == 0
    _, again, _ = run_cli(capsys, "--db", db, "alerts", "--json")
    assert first == again
    _, out, _ = run_cli(capsys, "--db", db, "replay", raw, "--until", "2026-09-30", "--json")
    assert json.loads(out)["days"] > 0


def test_slack_notifier_queues_one_message_per_case_event(tmp_path, capsys):
    db = tmp_path / "iw.db"
    run_cli(capsys, "--db", db, "replay", ROOT / "fixtures" / "raw", "--until", "2026-09-30", "--notifier", "slack")
    _, alerts, _ = run_cli(capsys, "--db", db, "alerts", "--json")
    _, outbox, _ = run_cli(capsys, "--db", db, "outbox", "--json")
    _, cases, _ = run_cli(capsys, "--db", db, "cases", "--json")
    assert len(json.loads(cases)) <= len(json.loads(outbox)) < len(json.loads(alerts))


def test_bad_date_exits_2(tmp_path, capsys):
    code, _, err = run_cli(capsys, "--db", tmp_path / "x.db", "replay", ROOT / "fixtures" / "raw", "--until", "nope")
    assert code == 2 and "YYYY-MM-DD" in err


def test_migrations_are_idempotent(tmp_path):
    conn = open_db(tmp_path / "m.db")
    assert migrate(conn) == []
    names = {r["name"] for r in conn.execute("SELECT name FROM schema_migrations")}
    assert "0001_baselines.sql" in names
