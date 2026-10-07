import pytest

from vetting import normalize
from vetting.cache import TTLCache
from vetting.errors import ConfigError
from vetting.lookups import LineType
from vetting.settings import DEFAULT_CONFIG_DIR, load_settings
from vetting.timeutil import parse_ts, to_iso


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("(415) 555-0143", "+14155550143"),
        ("415.555.0143", "+14155550143"),
        ("+1-415-555-0143 ext. 9", "+14155550143"),
        ("1 415 555 0143 x12", "+14155550143"),
        ("0044 20 7946 0105", "+442079460105"),
        ("+44 20 7946 0105", "+442079460105"),
        ("555-0143", None),
        ("", None),
        (None, None),
    ],
)
def test_phone_e164(raw, expected):
    assert normalize.phone_e164(raw) == expected


def test_email_key_drops_plus_tags_and_dots_for_dot_insensitive_domains():
    assert normalize.email_key(" Taylor.E+jobs@Mail.Example.org ") == "taylore@mail.example.org"
    assert normalize.email_key("a.b@example.com") == "a.b@example.com"
    assert normalize.email_key("not-an-email") is None
    assert normalize.email_domain("x@Burner.Example.org") == "burner.example.org"


def test_name_key_ignores_case_accents_punctuation_and_order():
    assert normalize.name_key("Zoë Testwood") == normalize.name_key("testwood, ZOE")
    assert normalize.name_key("Ann-Marie O'Neil") == normalize.name_key("o neil ann marie")
    assert normalize.name_key("A B") != normalize.name_key("A C")


def test_ip_prefix24_and_country():
    assert normalize.ip_prefix24("198.51.100.37") == "198.51.100.0/24"
    assert normalize.ip_prefix24("2001:db8:1:2::5") == "2001:db8:1::/48"
    assert normalize.ip_prefix24("nope") is None
    assert normalize.country_code("united states") == "US"
    assert normalize.country_code("gb") == "GB"


def test_parse_ts_converts_offsets_to_utc_and_rejects_naive():
    parsed = parse_ts("2026-09-14T10:22:00.000-07:00")
    assert to_iso(parsed) == "2026-09-14T17:22:00+00:00"
    assert to_iso(parse_ts("2026-09-14T17:22:00Z")) == "2026-09-14T17:22:00+00:00"
    with pytest.raises(ValueError):
        parse_ts("2026-09-14T10:22:00")


def test_ttl_cache_expires_and_reuses():
    now = [0.0]
    calls = []
    cache = TTLCache[int](10, clock=lambda: now[0])
    load = lambda key: calls.append(key) or len(calls)  # noqa: E731
    assert cache.get_or_load("a", load) == 1
    assert cache.get_or_load("a", load) == 1
    now[0] = 11
    assert cache.get_or_load("a", load) == 2


def test_lookups_read_fixture_intel(lookups):
    assert lookups.phone.lookup("+16465550102").line_type is LineType.VOIP
    assert lookups.phone.lookup("+19990000000").line_type is LineType.UNKNOWN
    vpn = lookups.ip.lookup("203.0.113.20")
    assert (vpn.is_vpn, vpn.asn) == (True, "AS64500")
    assert lookups.ip.lookup("198.51.100.5").country == "US"
    assert lookups.ip.lookup("10.0.0.1").country is None
    assert lookups.email.lookup("burner.example.org").disposable


def test_settings_merge_tenant_over_default_and_reject_unknown_sections(tmp_path):
    assert load_settings("acme", DEFAULT_CONFIG_DIR).weight("disposable_email") == 25
    assert load_settings("globex", DEFAULT_CONFIG_DIR).weight("disposable_email") == 20
    assert load_settings("globex", DEFAULT_CONFIG_DIR).highly_recommended_at == 45
    cfg = tmp_path / "config"
    (cfg / "tenants").mkdir(parents=True)
    (cfg / "default.toml").write_text((DEFAULT_CONFIG_DIR / "default.toml").read_text())
    (cfg / "tenants" / "typo.toml").write_text("[scorring]\nrecommended_at = 5\n")
    with pytest.raises(ConfigError):
        load_settings("typo", cfg)
    with pytest.raises(ConfigError):
        load_settings("Bad Tenant", cfg)
    with pytest.raises(ConfigError):
        load_settings("acme", DEFAULT_CONFIG_DIR).weight("no_such_signal")
