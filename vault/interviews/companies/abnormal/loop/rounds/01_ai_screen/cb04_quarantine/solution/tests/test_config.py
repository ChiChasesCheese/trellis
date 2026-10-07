from __future__ import annotations

import pytest

from quarantine.config import SettingsProvider, build_settings
from quarantine.errors import ConfigError


def test_tenant_overrides_merge_over_defaults():
    provider = SettingsProvider()
    acme, globex = provider.for_tenant("acme"), provider.for_tenant("globex")
    assert acme.decision.quarantine_at == 70
    assert globex.decision.quarantine_at == 60
    assert globex.decision.review_at == 40  # inherited
    assert "acme.test" in acme.domains


def test_unknown_tenant_is_a_config_error():
    with pytest.raises(ConfigError, match="unknown tenant"):
        SettingsProvider().for_tenant("nobody")


def test_bad_tenant_id_is_rejected():
    with pytest.raises(ConfigError, match="invalid tenant"):
        SettingsProvider().for_tenant("../etc")


def test_unknown_keys_are_errors():
    with pytest.raises(ConfigError, match="unknown keys"):
        build_settings("t", {"decision": {"quarantine_at": 80, "typo": 1}})
    with pytest.raises(ConfigError, match="unknown config keys"):
        build_settings("t", {"nonsense": {}})


def test_thresholds_must_be_ordered():
    with pytest.raises(ConfigError, match="review_at < quarantine_at"):
        build_settings("t", {"decision": {"quarantine_at": 30, "review_at": 40}})


def test_tenants_lists_files():
    assert SettingsProvider().tenants() == ["acme", "globex"]
