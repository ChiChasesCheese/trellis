import io
import logging
from datetime import datetime, timedelta, timezone

from insiderwatch.alerts import Alert, AlertStore
from insiderwatch.config import Config, load_config
from insiderwatch.errors import ConfigError
from insiderwatch.notify import build_notifier
from insiderwatch.notify.console import ConsoleNotifier, format_alert
from insiderwatch.notify.slack_webhook import read_outbox
from insiderwatch.scoring import decayed, score_finding, severity_label, user_risk
from insiderwatch.signals import Finding

import pytest

NOW = datetime(2026, 9, 30, 12, tzinfo=timezone.utc)


def finding(signal="volume_spike", strength=0.5):
    return Finding(signal=signal, user="ann@acme.example", ts=NOW, strength=strength, reasons=("r",))


def alert(score=0.5, ts=NOW, user="ann@acme.example"):
    return Alert(user=user, signal="volume_spike", score=score, ts=ts, reasons=["because"], evidence={"k": 1})


def test_score_uses_configured_weight(config):
    assert score_finding(finding(strength=0.5), config) == 0.45  # 0.9 * 0.5


def test_unknown_signal_falls_back_to_default_weight_and_warns(config, caplog):
    with caplog.at_level(logging.WARNING):
        assert score_finding(finding("brand_new", 1.0), config) == config.default_signal_weight
    assert "no weight configured" in caplog.text


def test_severity_labels(config):
    assert [severity_label(s, config) for s in (0.1, 0.4, 0.69, 0.7, 1.0)] == ["low", "medium", "medium", "high", "high"]


def test_decay_halves_each_half_life(config):
    old = NOW - timedelta(days=config.score_half_life_days)
    assert abs(decayed(0.8, old, NOW, config) - 0.4) < 1e-9
    assert user_risk([alert(0.8, old), alert(0.8, NOW)], NOW, config) == 1.2


def test_config_overrides_and_unknown_keys(tmp_path):
    good = tmp_path / "c.toml"
    good.write_text('alert_threshold = 0.5\n[signal_weights]\nvolume_spike = 0.1\n')
    cfg = load_config(good)
    assert cfg.alert_threshold == 0.5
    assert cfg.signal_weights["volume_spike"] == 0.1 and cfg.signal_weights["off_hours_activity"] == 0.4
    bad = tmp_path / "bad.toml"
    bad.write_text("nonsense = 1\n")
    with pytest.raises(ConfigError):
        load_config(bad)


def test_alert_store_roundtrip_and_user_filter(conn):
    store = AlertStore(conn)
    first = store.add(alert())
    store.add(alert(user="lee@acme.example"))
    assert first.id == 1
    assert store.get(1).reasons == ["because"] and store.get(1).evidence == {"k": 1}
    assert [a.user for a in store.list(user="ANN@acme.example")] == ["ann@acme.example"]
    assert len(store.list()) == 2


def test_console_notifier_formats_severity(config):
    out = io.StringIO()
    ConsoleNotifier(config, out).notify(alert(0.9))
    assert out.getvalue().startswith("[HIGH] ann@acme.example volume_spike")
    assert format_alert(alert(0.1), config).startswith("[LOW]")


def test_slack_notifier_writes_outbox(conn, config):
    notifier = build_notifier("slack", conn, config)
    notifier.notify(AlertStore(conn).add(alert()))
    rows = read_outbox(conn)
    assert len(rows) == 1 and rows[0]["payload"]["alert_id"] == 1


def test_unknown_notifier_is_a_config_error(conn, config):
    with pytest.raises(ConfigError):
        build_notifier("pager", conn, config)
