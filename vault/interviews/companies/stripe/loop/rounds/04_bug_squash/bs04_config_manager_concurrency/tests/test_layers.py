"""Unit tests for the two standalone layer loaders (no ConfigManager involved)."""

import json

from confmgr.layers import load_env_layer, load_file_layer


def test_load_file_layer_reads_json_object(tmp_path):
    f = tmp_path / "config.json"
    f.write_text(json.dumps({"greeting": "hi", "retries": 3}))
    assert load_file_layer(str(f)) == {"greeting": "hi", "retries": 3}


def test_load_file_layer_missing_file_returns_empty_dict(tmp_path):
    assert load_file_layer(str(tmp_path / "nope.json")) == {}


def test_load_file_layer_rejects_non_object_top_level(tmp_path):
    f = tmp_path / "config.json"
    f.write_text(json.dumps([1, 2, 3]))
    try:
        load_file_layer(str(f))
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a non-object JSON file")


def test_load_env_layer_strips_prefix_and_ignores_others(monkeypatch):
    monkeypatch.setenv("MYAPP_TIMEOUT", "30")
    monkeypatch.setenv("MYAPP_RETRIES", "5")
    monkeypatch.setenv("OTHER_VAR", "ignored")
    assert load_env_layer("MYAPP_") == {"TIMEOUT": "30", "RETRIES": "5"}


def test_load_env_layer_with_no_matches_returns_empty_dict(monkeypatch):
    monkeypatch.delenv("NOPE_ANYTHING", raising=False)
    assert load_env_layer("NOPE_") == {}
