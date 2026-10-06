import json
from pathlib import Path

from insiderwatch.config import Config
from insiderwatch.connectors import registered_connectors
from insiderwatch.events import Action


def load(root: Path, config=None):
    connector = registered_connectors()["gdrive"](root, config or Config())
    return connector, list(connector.events())


def test_gdrive_is_registered_and_pages_are_followed(fixtures_dir):
    connector, events = load(fixtures_dir / "raw" / "gdrive")
    assert connector.stats.fetched == 18
    assert connector.stats.emitted == len(events) == 10


def test_actions_and_sizes(fixtures_dir):
    _, events = load(fixtures_dir / "raw" / "gdrive")
    downloads = [e for e in events if e.action is Action.FILE_DOWNLOAD]
    assert len(downloads) == 6 and downloads[0].bytes == 2_048_000
    shares = [e for e in events if e.action is Action.FILE_SHARE_EXTERNAL]
    assert len(shares) == 4
    assert {e.attrs.get("visibility") or e.attrs["shared_with"] for e in shares} == {
        "people_with_link", "public_on_the_web", "partner@vendor.example", "someone.private@gmail.com"}


def test_unmapped_records_are_dropped_and_counted(fixtures_dir):
    connector, _ = load(fixtures_dir / "raw" / "gdrive")
    assert connector.stats.dropped["unmapped_event"] == 5  # view x2, edit, rename, sync_conflict
    assert connector.stats.dropped["no_user"] == 1
    assert connector.stats.dropped["internal_access_change"] == 1
    assert connector.stats.dropped["visibility_not_exposed"] == 1


def test_offsets_are_converted_to_utc_and_users_lowercased(fixtures_dir):
    _, events = load(fixtures_dir / "raw" / "gdrive")
    assert any(e.ts.isoformat() == "2026-09-22T16:30:00+00:00" for e in events)
    assert any(e.ts.isoformat() == "2026-10-01T03:00:00+00:00" for e in events)
    assert all(e.user == e.user.lower() for e in events)


def test_item_with_two_events_yields_both(tmp_path):
    item = {"id": {"time": "2026-09-01T10:00:00Z"}, "actor": {"email": "a@acme.example"},
            "events": [{"name": "view", "parameters": []},
                       {"name": "download", "parameters": [{"name": "file_size", "intValue": "5"}]}]}
    (tmp_path / "page-0001.json").write_text(json.dumps({"items": [item]}))
    connector, events = load(tmp_path)
    assert [e.bytes for e in events] == [5] and connector.stats.dropped_total == 1


def test_replay_includes_gdrive_automatically(tmp_path, fixtures_dir):
    from insiderwatch.cli import main
    import contextlib, io

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        main(["--db", str(tmp_path / "x.db"), "replay", str(fixtures_dir / "raw"), "--until", "2026-09-30", "--json"])
    assert json.loads(out.getvalue())["by_source"]["gdrive"] == 9  # the 20:00-07:00 event is already Oct 1 UTC
