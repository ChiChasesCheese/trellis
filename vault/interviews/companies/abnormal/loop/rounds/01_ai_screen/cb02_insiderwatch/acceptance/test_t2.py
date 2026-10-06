"""t2: group alerts into cases. Observed through `cases [--user U] --json`, `alerts --json`, `outbox --json`."""
import json
import subprocess
import sys

import pytest

def iw(root, db, *args):
    """Run `python -m insiderwatch --db DB <args>` inside the codebase; returns CompletedProcess."""
    return subprocess.run([sys.executable, "-m", "insiderwatch", "--db", str(db), *map(str, args)],
                          cwd=root, capture_output=True, text=True, timeout=120)


def iw_json(root, db, *args):
    proc = iw(root, db, *args)
    assert proc.returncode == 0, f"insiderwatch {args} failed: {proc.stderr[-400:]}"
    return json.loads(proc.stdout)


HENRY = "henry.ross@acme.example"  # two night bursts: 09-02..09-03 (45 alerts) and 09-27 (22 alerts)
ORDER = {"low": 0, "medium": 1, "high": 2}


_DB = {}  # replay once per codebase under test


@pytest.fixture
def db(tmp_path_factory, codebase_root_path):
    key = str(codebase_root_path)
    if key not in _DB:
        path = tmp_path_factory.mktemp("t2") / "iw.db"
        proc = iw(codebase_root_path, path, "replay", "fixtures/raw", "--until", "2026-09-30", "--notifier", "slack")
        assert proc.returncode == 0, proc.stderr[-400:]
        _DB[key] = path
    return _DB[key]


def cases(root, db, *extra):
    return iw_json(root, db, "cases", *extra, "--json")


@pytest.mark.t2
@pytest.mark.core
def test_every_alert_lands_in_exactly_one_case(codebase_root_path, db):
    all_alerts = iw_json(codebase_root_path, db, "alerts", "--json")
    members = [i for c in cases(codebase_root_path, db) for i in c["alerts"]]
    assert sorted(members) == sorted(a["id"] for a in all_alerts)


@pytest.mark.t2
@pytest.mark.core
def test_cases_never_mix_users(codebase_root_path, db):
    owner = {a["id"]: a["user"] for a in iw_json(codebase_root_path, db, "alerts", "--json")}
    for c in cases(codebase_root_path, db):
        assert {owner[i] for i in c["alerts"]} == {c["user"]}


@pytest.mark.t2
@pytest.mark.core
def test_forty_alerts_collapse_into_a_handful_of_cases(codebase_root_path, db):
    found = cases(codebase_root_path, db, "--user", HENRY)
    n_alerts = len(iw_json(codebase_root_path, db, "alerts", "--user", HENRY, "--json"))
    assert n_alerts >= 40 and 1 <= len(found) <= 3


@pytest.mark.t2
@pytest.mark.core
def test_user_filter_returns_only_that_user(codebase_root_path, db):
    found = cases(codebase_root_path, db, "--user", HENRY)
    assert found and {c["user"] for c in found} == {HENRY}
    assert len(cases(codebase_root_path, db)) > len(found)


@pytest.mark.t2
@pytest.mark.core
def test_case_severity_is_at_least_its_worst_alert(codebase_root_path, db):
    by_id = {a["id"]: a for a in iw_json(codebase_root_path, db, "alerts", "--json")}
    for c in cases(codebase_root_path, db):
        assert c["severity"] in ORDER and c["status"] == "open"
        worst = max(ORDER[by_id[i]["severity"]] for i in c["alerts"])
        assert ORDER[c["severity"]] >= worst, "one high alert among many low ones must not be averaged away"


@pytest.mark.t2
@pytest.mark.core
def test_notifications_are_per_case_not_per_alert(codebase_root_path, db):
    outbox = iw_json(codebase_root_path, db, "outbox", "--json")
    n_alerts = len(iw_json(codebase_root_path, db, "alerts", "--json"))
    n_cases = len(cases(codebase_root_path, db))
    assert n_cases <= len(outbox) <= n_alerts // 2


@pytest.mark.t2
@pytest.mark.stretch
def test_separate_bursts_weeks_apart_are_separate_cases(codebase_root_path, db):
    found = cases(codebase_root_path, db, "--user", HENRY)
    assert len(found) == 2 and found[0]["alerts"][0] < found[1]["alerts"][0]


@pytest.mark.t2
@pytest.mark.stretch
def test_closed_case_stays_closed_and_new_alerts_open_a_new_one(tmp_path, codebase_root_path):
    db = tmp_path / "iw.db"
    assert iw(codebase_root_path, db, "replay", "fixtures/raw", "--until", "2026-09-02").returncode == 0
    (first,) = cases(codebase_root_path, db, "--user", HENRY)
    assert iw(codebase_root_path, db, "cases", "close", first["id"]).returncode == 0
    assert iw(codebase_root_path, db, "replay", "fixtures/raw", "--until", "2026-09-03").returncode == 0
    found = cases(codebase_root_path, db, "--user", HENRY)
    assert [c["status"] for c in found] == ["closed", "open"]
    assert found[0]["alerts"] == first["alerts"] and found[1]["alerts"]


@pytest.mark.t2
@pytest.mark.stretch
def test_escalation_of_an_open_case_notifies_again(tmp_path, codebase_root_path):
    db = tmp_path / "iw.db"
    assert iw(codebase_root_path, db, "replay", "fixtures/raw", "--until", "2026-09-02", "--notifier", "slack").returncode == 0
    assert len(cases(codebase_root_path, db)) == 1
    assert len(iw_json(codebase_root_path, db, "outbox", "--json")) >= 2, "low-severity case opened, then a high alert arrived"


@pytest.mark.t2
@pytest.mark.regression
def test_alerts_command_still_lists_every_alert_individually(codebase_root_path, db):
    assert len(iw_json(codebase_root_path, db, "alerts", "--user", HENRY, "--json")) >= 40


@pytest.mark.t2
@pytest.mark.regression
def test_replaying_again_changes_nothing(tmp_path, codebase_root_path):
    db = tmp_path / "iw.db"
    iw(codebase_root_path, db, "replay", "fixtures/raw", "--until", "2026-09-30")
    before = iw_json(codebase_root_path, db, "alerts", "--json")
    assert iw(codebase_root_path, db, "replay", "fixtures/raw", "--until", "2026-09-30").returncode == 0
    assert iw_json(codebase_root_path, db, "alerts", "--json") == before
