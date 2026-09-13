"""ConfigManager tests: layer precedence, runtime overrides, and reload()."""

import json

from confmgr.manager import ConfigManager


# ---------------------------------------------------------------- basic get / precedence
def test_get_returns_default_for_undefined_key():
    mgr = ConfigManager(defaults={})
    assert mgr.get("nope", default="fallback") == "fallback"


def test_get_returns_default_none_when_not_given():
    mgr = ConfigManager(defaults={})
    assert mgr.get("nope") is None


def test_defaults_layer_is_used_when_nothing_overrides_it():
    mgr = ConfigManager(defaults={"greeting": "hi"})
    assert mgr.get("greeting") == "hi"


def test_file_layer_overrides_defaults(tmp_path):
    f = tmp_path / "config.json"
    f.write_text(json.dumps({"greeting": "bonjour"}))
    mgr = ConfigManager(defaults={"greeting": "hi"}, file_path=str(f))
    assert mgr.get("greeting") == "bonjour"


def test_env_layer_overrides_file_layer(tmp_path, monkeypatch):
    f = tmp_path / "config.json"
    f.write_text(json.dumps({"greeting": "bonjour"}))
    monkeypatch.setenv("MYAPP_GREETING", "hola")
    mgr = ConfigManager(defaults={"greeting": "hi"}, file_path=str(f), env_prefix="MYAPP_")
    assert mgr.get("GREETING") == "hola"


def test_runtime_override_has_highest_precedence(tmp_path, monkeypatch):
    f = tmp_path / "config.json"
    f.write_text(json.dumps({"greeting": "bonjour"}))
    monkeypatch.setenv("MYAPP_GREETING", "hola")
    mgr = ConfigManager(defaults={"greeting": "hi"}, file_path=str(f), env_prefix="MYAPP_")
    mgr.set_override("GREETING", "howdy")
    assert mgr.get("GREETING") == "howdy"


def test_clear_override_falls_back_to_next_layer(tmp_path):
    f = tmp_path / "config.json"
    f.write_text(json.dumps({"greeting": "bonjour"}))
    mgr = ConfigManager(defaults={"greeting": "hi"}, file_path=str(f))
    mgr.set_override("greeting", "howdy")
    assert mgr.get("greeting") == "howdy"
    mgr.clear_override("greeting")
    assert mgr.get("greeting") == "bonjour"


def test_repeated_get_returns_same_value_from_cache():
    mgr = ConfigManager(defaults={"x": 1})
    assert mgr.get("x") == 1
    assert mgr.get("x") == 1


# ---------------------------------------------------------------- reload()
def test_reload_without_file_or_env_is_a_no_op():
    mgr = ConfigManager(defaults={"x": 1})
    mgr.reload()  # must not raise
    assert mgr.get("x") == 1


def test_reload_picks_up_new_file_contents_immediately(tmp_path):
    f = tmp_path / "config.json"
    f.write_text(json.dumps({"greeting": "hi"}))
    mgr = ConfigManager(defaults={}, file_path=str(f), cache_ttl=100)

    assert mgr.get("greeting") == "hi"

    f.write_text(json.dumps({"greeting": "bonjour"}))
    mgr.reload()

    assert mgr.get("greeting") == "bonjour"


def test_get_int_converts_env_string_to_int(monkeypatch):
    monkeypatch.setenv("MYAPP_TIMEOUT", "30")
    mgr = ConfigManager(defaults={}, env_prefix="MYAPP_")
    assert mgr.get_int("TIMEOUT") == 30


def test_get_int_returns_default_for_missing_key():
    mgr = ConfigManager(defaults={})
    assert mgr.get_int("nope", default=7) == 7


def test_get_int_raises_on_unparseable_value():
    mgr = ConfigManager(defaults={"x": "not-a-number"})
    try:
        mgr.get_int("x")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a non-numeric value")


def test_get_bool_accepts_common_spellings(monkeypatch):
    monkeypatch.setenv("MYAPP_DEBUG", "Yes")
    mgr = ConfigManager(defaults={}, env_prefix="MYAPP_")
    assert mgr.get_bool("DEBUG") is True


def test_get_bool_passes_through_a_native_bool():
    mgr = ConfigManager(defaults={"flag": False})
    assert mgr.get_bool("flag") is False


def test_snapshot_includes_keys_from_every_layer(tmp_path):
    f = tmp_path / "config.json"
    f.write_text(json.dumps({"from_file": "f"}))
    mgr = ConfigManager(defaults={"from_defaults": "d"}, file_path=str(f))
    mgr.set_override("from_override", "o")
    snap = mgr.snapshot()
    assert snap == {"from_defaults": "d", "from_file": "f", "from_override": "o"}


def test_reload_replaces_env_layer_contents(monkeypatch):
    """Checks reload() at the layer level (bypassing get()/the cache entirely) -- this is about
    whether reload() actually re-reads os.environ into a fresh dict, independent of whatever
    get() does with a previously-cached value for the same key (covered above)."""
    monkeypatch.setenv("MYAPP_A", "1")
    mgr = ConfigManager(defaults={}, env_prefix="MYAPP_")
    assert mgr._env_layer == {"A": "1"}

    monkeypatch.setenv("MYAPP_A", "2")
    monkeypatch.setenv("MYAPP_B", "3")
    mgr.reload()

    assert mgr._env_layer == {"A": "2", "B": "3"}
