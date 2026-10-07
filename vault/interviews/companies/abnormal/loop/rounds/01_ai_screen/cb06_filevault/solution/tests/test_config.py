import pytest

from filevault.config import load_settings
from filevault.errors import ConfigError


def test_defaults():
    s = load_settings({})
    assert s.quota_bytes_per_user == 10 * 1024 * 1024
    assert s.max_upload_bytes == 10 * 1024 * 1024
    assert s.admin_users == ("admin",)
    assert s.rate_limit_per_sec == 50.0


def test_env_overrides():
    s = load_settings(
        {"FILEVAULT_QUOTA_BYTES_PER_USER": "1000", "FILEVAULT_ADMIN_USERS": "ops, root"}
    )
    assert s.quota_bytes_per_user == 1000
    assert s.admin_users == ("ops", "root")


@pytest.mark.parametrize(
    "env",
    [
        {"FILEVAULT_MAX_UPLOAD_BYTES": "lots"},
        {"FILEVAULT_MAX_UPLOAD_BYTES": "0"},
        {"FILEVAULT_RATE_LIMIT_PER_SEC": "-1"},
        {"FILEVAULT_DEFAULT_PAGE_SIZE": "500"},
    ],
)
def test_invalid_values_raise(env):
    with pytest.raises(ConfigError):
        load_settings(env)


def test_unknown_key_in_file_raises(tmp_path):
    path = tmp_path / "c.toml"
    path.write_text("surprise = 1\n")
    with pytest.raises(ConfigError):
        load_settings({}, path)


def test_quota_override_applies_to_the_app(tmp_path):
    from filevault.app import create_app

    app = create_app(tmp_path / "d", env={"FILEVAULT_QUOTA_BYTES_PER_USER": "7"})
    try:
        assert app.settings.quota_bytes_per_user == 7
    finally:
        app.close()
