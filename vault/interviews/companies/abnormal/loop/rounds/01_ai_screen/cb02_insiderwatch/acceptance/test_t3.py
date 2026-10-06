"""t3: Google Drive audit-log source. Observed through `replay --json` summaries only."""
import json
import shutil
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


def replay(root, tmp_path, raw, until="2026-10-02", name="iw.db"):
    return iw_json(root, tmp_path / name, "replay", raw, "--until", until, "--json")


@pytest.fixture
def gdrive_only(tmp_path, codebase_root_path):
    raw = tmp_path / "raw"
    shutil.copytree(codebase_root_path / "fixtures" / "raw" / "gdrive", raw / "gdrive")
    return raw


def page(items, nxt=None):
    out = {"kind": "admin#reports#activities", "items": items}
    if nxt:
        out["nextPageToken"] = nxt
    return out


def item(time, name, email="x@acme.example", **params):
    return {"id": {"time": time}, "actor": {"email": email}, "events": [
        {"name": name, "parameters": [{"name": k, "intValue": str(v)} if isinstance(v, int) else {"name": k, "value": v}
                                      for k, v in params.items()]}]}


@pytest.mark.t3
@pytest.mark.core
def test_gdrive_events_are_ingested_across_pages(codebase_root_path, tmp_path, gdrive_only):
    assert replay(codebase_root_path, tmp_path, gdrive_only)["by_source"]["gdrive"] == 10


@pytest.mark.t3
@pytest.mark.core
def test_downloads_are_mapped(codebase_root_path, tmp_path, gdrive_only):
    assert replay(codebase_root_path, tmp_path, gdrive_only)["by_action"]["FILE_DOWNLOAD"] == 6


@pytest.mark.t3
@pytest.mark.core
def test_link_public_and_external_user_shares_are_external_shares(codebase_root_path, tmp_path, gdrive_only):
    # people_with_link, public_on_the_web, partner@vendor.example, someone.private@gmail.com;
    # NOT: visibility -> private, access granted to a colleague
    assert replay(codebase_root_path, tmp_path, gdrive_only)["by_action"]["FILE_SHARE_EXTERNAL"] == 4


@pytest.mark.t3
@pytest.mark.core
def test_unmodelled_events_are_dropped_and_counted(codebase_root_path, tmp_path, gdrive_only):
    summary = replay(codebase_root_path, tmp_path, gdrive_only)
    assert summary["dropped"]["gdrive"] >= 6  # view x2, edit, rename, unknown event, actor without email


@pytest.mark.t3
@pytest.mark.core
def test_every_event_of_a_multi_event_item_is_handled(codebase_root_path, tmp_path):
    raw = tmp_path / "raw" / "gdrive"
    raw.mkdir(parents=True)
    both = item("2026-09-01T17:00:00Z", "view")
    both["events"].append(item("x", "download", file_size=5)["events"][0])
    (raw / "page-0001.json").write_text(json.dumps(page([both])))
    summary = replay(codebase_root_path, tmp_path, raw.parent)
    assert summary["by_action"] == {"FILE_DOWNLOAD": 1} and summary["dropped"]["gdrive"] == 1


@pytest.mark.t3
@pytest.mark.core
def test_three_pages_are_followed(codebase_root_path, tmp_path):
    raw = tmp_path / "raw" / "gdrive"
    raw.mkdir(parents=True)
    for i in (1, 2, 3):
        nxt = f"page-000{i + 1}.json" if i < 3 else None
        (raw / f"page-000{i}.json").write_text(json.dumps(page([item(f"2026-09-0{i}T17:00:00Z", "download")], nxt)))
    assert replay(codebase_root_path, tmp_path, raw.parent)["by_action"] == {"FILE_DOWNLOAD": 3}


@pytest.mark.t3
@pytest.mark.core
def test_replay_picks_gdrive_up_without_any_flag(codebase_root_path, tmp_path):
    summary = replay(codebase_root_path, tmp_path, codebase_root_path / "fixtures" / "raw")
    assert {"gdrive", "m365_audit", "okta", "slack_audit"} <= set(summary["by_source"])


@pytest.mark.t3
@pytest.mark.stretch
def test_utc_offsets_are_honoured_by_until(codebase_root_path, tmp_path, gdrive_only):
    # kim's download at 2026-09-30T20:00:00-07:00 is already 10-01 03:00 UTC
    summary = replay(codebase_root_path, tmp_path, gdrive_only, until="2026-09-30")
    assert summary["by_action"]["FILE_DOWNLOAD"] == 5 and summary["by_source"]["gdrive"] == 9


@pytest.mark.t3
@pytest.mark.regression
def test_existing_sources_are_unchanged(codebase_root_path, tmp_path):
    summary = replay(codebase_root_path, tmp_path, codebase_root_path / "fixtures" / "raw", until="2026-09-30")
    assert (summary["by_source"]["m365_audit"], summary["by_source"]["okta"], summary["by_source"]["slack_audit"]) == (1410, 257, 25)
    assert summary["dropped"]["m365_audit"] == 27 and summary["dropped"]["slack_audit"] == 8


@pytest.mark.t3
@pytest.mark.regression
def test_directories_without_a_connector_are_ignored(codebase_root_path, tmp_path, gdrive_only):
    (gdrive_only / "mystery").mkdir()
    (gdrive_only / "mystery" / "page-0001.json").write_text("{}")
    assert "mystery" not in replay(codebase_root_path, tmp_path, gdrive_only)["by_source"]
