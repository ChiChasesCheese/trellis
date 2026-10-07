"""t1: flag departing employees who are taking data. Observed only through replay + `alerts --json`."""
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


CAROL = "carol.diaz@acme.example"   # gave notice 09-11, last day 09-26, shares/forwards to gmail in her last week
ERIN = "erin.walsh@acme.example"    # laid off (last day 10-05, no resignation), copies data out 09-28..09-30
BOB = "bob.martin@acme.example"     # resigned, heavy downloader, behaving exactly as usual
DAVE = "dave.kim@acme.example"      # partnerships, shares externally every day, being laid off, behaving as usual
FRANK = "frank.okafor@acme.example"  # starts sharing externally but is not leaving
GINA = "gina.park@acme.example"     # terminated 09-18, account still active on 09-22/23
ALICE = "alice.nguyen@acme.example"


_DB = {}  # replay once per codebase under test


@pytest.fixture
def db(tmp_path_factory, codebase_root_path):
    key = str(codebase_root_path)
    if key not in _DB:
        path = tmp_path_factory.mktemp("t1") / "iw.db"
        proc = iw(codebase_root_path, path, "replay", "fixtures/raw", "--until", "2026-09-30", "--json")
        assert proc.returncode == 0, proc.stderr[-400:]
        _DB[key] = path
    return _DB[key]


def alerts_for(root, db, user):
    return iw_json(root, db, "alerts", "--user", user, "--json")


@pytest.mark.t1
@pytest.mark.core
def test_resigned_employee_exfiltrating_in_final_week_is_flagged(codebase_root_path, db):
    found = alerts_for(codebase_root_path, db, CAROL)
    assert found, "carol shares company files with her personal gmail in her last week and nothing fired"
    assert all("2026-09-11" <= a["ts"][:10] <= "2026-09-26" for a in found)


@pytest.mark.t1
@pytest.mark.core
def test_layoff_without_resignation_date_is_flagged_from_termination_date(codebase_root_path, db):
    found = alerts_for(codebase_root_path, db, ERIN)
    assert found and min(a["ts"][:10] for a in found) >= "2026-09-21"


@pytest.mark.t1
@pytest.mark.core
def test_heavy_user_behaving_normally_is_not_flagged(codebase_root_path, db):
    assert alerts_for(codebase_root_path, db, CAROL), "the departing exfiltrator must be caught before judging the false positives"
    assert alerts_for(codebase_root_path, db, BOB) == [], "bob downloads ~200MB/day every day: that is his baseline"


@pytest.mark.t1
@pytest.mark.core
def test_habitual_external_sharer_is_not_flagged(codebase_root_path, db):
    assert alerts_for(codebase_root_path, db, ERIN), "erin (new external sharing, laid off) must be caught before judging dave"
    assert alerts_for(codebase_root_path, db, DAVE) == [], "dave shares externally daily; leaving does not change that"


@pytest.mark.t1
@pytest.mark.core
def test_flag_is_stable_across_replays(codebase_root_path, db):
    before = alerts_for(codebase_root_path, db, CAROL)
    assert before
    assert iw(codebase_root_path, db, "replay", "fixtures/raw", "--until", "2026-09-30").returncode == 0
    assert alerts_for(codebase_root_path, db, CAROL) == before


@pytest.mark.t1
@pytest.mark.core
def test_flag_explains_itself_with_reasons_and_severity(codebase_root_path, db):
    found = alerts_for(codebase_root_path, db, CAROL)
    assert found
    for a in found:
        assert a["reasons"] and all(isinstance(r, str) and r for r in a["reasons"])
        assert a["score"] > 0 and a["severity"] in {"low", "medium", "high"}


@pytest.mark.t1
@pytest.mark.stretch
def test_activity_after_termination_is_flagged(codebase_root_path, db):
    found = alerts_for(codebase_root_path, db, GINA)
    assert found and all(a["ts"][:10] >= "2026-09-22" for a in found), "gina was terminated 09-18; her account is still being used"
    assert max(a["score"] for a in found) >= max(a["score"] for a in alerts_for(codebase_root_path, db, CAROL))


@pytest.mark.t1
@pytest.mark.stretch
def test_unusual_sharing_by_someone_not_leaving_is_not_a_departure_alert(codebase_root_path, db):
    assert alerts_for(codebase_root_path, db, FRANK) == []


@pytest.mark.t1
@pytest.mark.regression
def test_existing_signals_still_fire(codebase_root_path, db):
    signals = {a["signal"] for a in alerts_for(codebase_root_path, db, ALICE)}
    assert signals == {"volume_spike", "off_hours_activity", "unusual_login_location"}


@pytest.mark.t1
@pytest.mark.regression
def test_night_burst_user_still_alerts_and_bystanders_stay_quiet(codebase_root_path, db):
    assert len(alerts_for(codebase_root_path, db, "henry.ross@acme.example")) >= 40
    assert alerts_for(codebase_root_path, db, "olivia.chen@acme.example") == []
