import json
from datetime import datetime, timezone

import pytest

from insiderwatch.config import Config
from insiderwatch.connectors import registered_connectors
from insiderwatch.connectors.base import Connector, RawRecord
from insiderwatch.errors import ConnectorError
from insiderwatch.events import Action


def run(source, fixtures_dir, config=None):
    connector = registered_connectors()[source](fixtures_dir / "raw" / source, config or Config())
    return connector, list(connector.events())


def test_registry_has_the_shipped_sources():
    assert {"m365_audit", "okta", "slack_audit"} <= set(registered_connectors())


def test_m365_pages_are_followed_and_mapped(fixtures_dir):
    connector, events = run("m365_audit", fixtures_dir)
    assert len(list((fixtures_dir / "raw" / "m365_audit").glob("page-*.json"))) > 1
    assert connector.stats.fetched == connector.stats.emitted + connector.stats.dropped_total
    actions = {e.action for e in events}
    assert {Action.FILE_DOWNLOAD, Action.FILE_SHARE_EXTERNAL, Action.EMAIL_FORWARD_EXTERNAL} <= actions
    assert all(e.ts.tzinfo is not None and e.user == e.user.lower() for e in events)


def test_m365_internal_share_and_unknown_ops_are_dropped_and_counted(fixtures_dir):
    connector, _ = run("m365_audit", fixtures_dir)
    assert connector.stats.dropped["internal_share"] > 0
    assert connector.stats.dropped["unmapped_operation"] > 0


def test_m365_forward_to_internal_address_is_not_external(tmp_path):
    root = tmp_path / "m365_audit"
    root.mkdir()
    rec = {"Id": "1", "CreationTime": "2026-09-01T14:00:00", "Operation": "New-InboxRule", "UserId": "A@acme.example",
           "Parameters": [{"Name": "ForwardTo", "Value": "boss@acme.example"}]}
    (root / "page-0001.json").write_text(json.dumps({"Records": [rec]}))
    connector = registered_connectors()["m365_audit"](root, Config())
    assert list(connector.events()) == []
    assert connector.stats.dropped_total == 1


def test_okta_failure_outcome_maps_to_login_failed(fixtures_dir):
    _, events = run("okta", fixtures_dir)
    assert any(e.action is Action.LOGIN_FAILED for e in events)
    assert all(e.attrs["country"] for e in events if e.action is Action.LOGIN)


def test_slack_epoch_timestamps_are_utc(fixtures_dir):
    _, events = run("slack_audit", fixtures_dir)
    assert events and all(e.ts.utcoffset().total_seconds() == 0 for e in events)
    assert any(e.action is Action.MESSAGE_EXPORT for e in events)


def test_since_filters_events(fixtures_dir):
    connector = registered_connectors()["okta"](fixtures_dir / "raw" / "okta", Config())
    cutoff = datetime(2026, 9, 20, tzinfo=timezone.utc)
    assert all(e.ts >= cutoff for e in connector.events(since=cutoff))


def test_paging_loop_is_an_error(tmp_path):
    (tmp_path / "page-0001.json").write_text(json.dumps({"data": [], "next": "page-0001.json"}))
    connector = registered_connectors()["okta"](tmp_path, Config())
    with pytest.raises(ConnectorError):
        list(connector.events())


def test_none_without_drop_is_still_counted(tmp_path):
    class Quiet(Connector):
        source = "quiet"

        def parse_page(self, payload):
            return payload["rows"], None

        def normalize(self, raw: RawRecord):
            return None

    (tmp_path / "page-0001.json").write_text(json.dumps({"rows": [{}, {}]}))
    connector = Quiet(tmp_path, Config())
    assert list(connector.events()) == []
    assert connector.stats.dropped["unspecified"] == 2
