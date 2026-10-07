"""Intel feeds, address helpers and time helpers."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from rulelang.addresses import domain_of, host_of, is_internal, normalize_address
from rulelang.config import load_settings
from rulelang.errors import ConfigError
from rulelang.intel import IntelStore
from rulelang.timeutil import iso, parse_ts


def test_intel_lookups():
    intel = IntelStore(load_settings("acme").intel)
    assert "login-secure.evil-payments.example" in intel.bad_hosts
    assert intel.domain_age_days("Fresh-Supplier.example") == 3
    assert intel.domain_age_days("never-seen.example") is None
    assert "acme-vendor.example" in intel.vendors


def test_missing_feed_is_a_config_error(tmp_path):
    settings = load_settings("acme", fixtures_dir=tmp_path)
    with pytest.raises(ConfigError, match="bad_hosts.json"):
        IntelStore(settings.intel).bad_hosts  # noqa: B018


def test_address_helpers():
    assert normalize_address(" Dana <DANA@Acme.Example> ") == "dana@acme.example"
    assert domain_of("dana@acme.example") == "acme.example" and domain_of("nobody") == ""
    assert is_internal("a@globex-eu.example", ["globex.example", "globex-eu.example"])
    assert host_of("HTTPS://Login.Evil.example:8443/x?y=1") == "login.evil.example"


def test_timestamps_round_trip_in_utc():
    dt = parse_ts("2026-09-01T10:00:00-05:00")
    assert dt == datetime(2026, 9, 1, 15, 0, tzinfo=timezone.utc)
    assert iso(dt) == "2026-09-01T15:00:00+00:00"
    assert parse_ts("2026-09-01T10:00:00") == datetime(2026, 9, 1, 10, 0, tzinfo=timezone.utc)
