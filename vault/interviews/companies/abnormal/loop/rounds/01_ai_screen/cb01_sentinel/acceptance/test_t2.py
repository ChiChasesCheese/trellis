"""t2 -- enrichment plugins. New names: [enrichment] plugin_dirs / enabled in tenant config."""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cb01_support import BOTNET_C2, T0, US, build_env, login, travel  # noqa: E402

pytestmark = pytest.mark.t2

BUILTINS = ["geo", "history", "threat_intel"]

ASN_OWNER = '''
from sentinel.enrichment.base import Enricher


class AsnOwner(Enricher):
    name = "asn_owner"
    requires = ("geo",)

    def enrich(self, event, ctx):
        asn = event.enrichment["geo"].get("asn")  # raises KeyError if geo has not run yet
        return {"owner": f"AS{asn}-corp"} if asn else {}
'''

RISK_TAG = '''
from sentinel.enrichment.base import Enricher


class RiskTag(Enricher):
    name = "risk_tag"
    requires = ("asn_owner",)

    def enrich(self, event, ctx):
        return {"tag": "tagged:" + event.enrichment["asn_owner"]["owner"]}
'''

EXPLODING = '''
from sentinel.enrichment.base import Enricher


class Exploding(Enricher):
    name = "exploding"

    def enrich(self, event, ctx):
        raise RuntimeError("customer plugin bug")
'''


def plugin_dir(tmp_path: Path, name: str = "plugins", **files: str) -> Path:
    d = tmp_path / name
    d.mkdir(exist_ok=True)
    for stem, source in files.items():
        (d / f"{stem}.py").write_text(textwrap.dedent(source))
    return d


def enrichment_toml(dirs: list[Path], enabled: list[str] | None) -> str:
    lines = ["[enrichment]", "plugin_dirs = [" + ", ".join(f'"{d}"' for d in dirs) + "]"]
    if enabled is not None:
        lines.append("enabled = [" + ", ".join(f'"{n}"' for n in enabled) + "]")
    return "\n".join(lines) + "\n"


def event_enrichment(env, tenant: str, event_id: str) -> dict:
    resp = env.client(tenant).get(f"/events/{event_id}")
    assert resp.status_code == 200, resp.json
    return resp.json["enrichment"]


@pytest.fixture
def root(codebase_root_path):
    return codebase_root_path


@pytest.mark.regression
def test_default_config_still_runs_the_builtins(root, tmp_path):
    env = build_env(root, tmp_path)
    env.ingest("acme", travel("acme", "alice@acme.test"))
    enr = event_enrichment(env, "acme", "alice@acme.test-via")
    assert enr["geo"]["country"] == "DE" and "history" in enr and "threat_intel" in enr
    assert len(env.alerts("acme", rule="impossible_travel")) == 1


@pytest.mark.core
def test_enabled_plugin_result_lands_on_the_event(root, tmp_path):
    d = plugin_dir(tmp_path, asn_owner=ASN_OWNER)
    env = build_env(root, tmp_path, {"acme": enrichment_toml([d], BUILTINS + ["asn_owner"])})
    env.ingest("acme", [login("e1", "acme", T0, "alice@acme.test", US)])
    assert event_enrichment(env, "acme", "e1")["asn_owner"] == {"owner": "AS64500-corp"}
    assert event_enrichment(env, "acme", "e1")["geo"]["country"] == "US"  # built-ins still ran


@pytest.mark.core
def test_plugin_that_is_not_enabled_does_not_run(root, tmp_path):
    d = plugin_dir(tmp_path, asn_owner=ASN_OWNER)
    env = build_env(root, tmp_path, {"acme": enrichment_toml([d], BUILTINS)})
    env.ingest("acme", [login("e1", "acme", T0, "alice@acme.test", US)])
    assert "asn_owner" not in event_enrichment(env, "acme", "e1")


@pytest.mark.core
def test_requires_decides_order_not_the_enabled_list(root, tmp_path):
    d = plugin_dir(tmp_path, asn_owner=ASN_OWNER)
    env = build_env(root, tmp_path, {"acme": enrichment_toml([d], ["asn_owner", "history", "threat_intel", "geo"])})
    env.ingest("acme", [login("e1", "acme", T0, "alice@acme.test", US)])
    enr = event_enrichment(env, "acme", "e1")
    assert enr["asn_owner"]["owner"] == "AS64500-corp"  # geo ran first although it was listed last
    assert "history" in enr


@pytest.mark.core
def test_disabling_geo_quietly_stops_impossible_travel(root, tmp_path):
    d = plugin_dir(tmp_path)
    env = build_env(root, tmp_path, {"acme": enrichment_toml([d], ["threat_intel"])})
    env.ingest("acme", travel("acme", "alice@acme.test"), [login("c2", "acme", T0, "carol@acme.test", BOTNET_C2)])
    enr = event_enrichment(env, "acme", "alice@acme.test-via")
    assert "geo" not in enr or not enr["geo"]  # geo did not run
    assert env.alerts("acme", rule="impossible_travel") == []
    assert len(env.alerts("acme", rule="known_bad_ip")) == 1  # the pipeline kept going


@pytest.mark.core
def test_a_crashing_plugin_does_not_stop_the_pipeline(root, tmp_path):
    d = plugin_dir(tmp_path, asn_owner=ASN_OWNER, exploding=EXPLODING)
    env = build_env(root, tmp_path, {"acme": enrichment_toml([d], BUILTINS + ["exploding", "asn_owner"])})
    env.ingest("acme", travel("acme", "alice@acme.test"))
    enr = event_enrichment(env, "acme", "alice@acme.test-via")
    assert enr["asn_owner"]["owner"].startswith("AS")  # enrichers after the crashing one still ran
    assert len(env.alerts("acme", rule="impossible_travel")) == 1


@pytest.mark.core
def test_unknown_enricher_name_is_a_configuration_error(root, tmp_path):
    from sentinel.config import ConfigError

    d = plugin_dir(tmp_path, asn_owner=ASN_OWNER)
    good = build_env(root, tmp_path / "good", {"acme": enrichment_toml([d], BUILTINS + ["asn_owner"])})
    good.ingest("acme", [login("e1", "acme", T0, "alice@acme.test", US)])
    assert "asn_owner" in event_enrichment(good, "acme", "e1")  # the same shape of config, valid names: fine

    with pytest.raises(ConfigError) as err:
        bad = build_env(root, tmp_path / "bad", {"acme": enrichment_toml([d], BUILTINS + ["asn_ownr"])})
        bad.ingest("acme", [login("e1", "acme", T0, "alice@acme.test", US)])
    assert "asn_ownr" in str(err.value)


@pytest.mark.core
def test_tenants_do_not_share_plugins(root, tmp_path):
    d = plugin_dir(tmp_path, asn_owner=ASN_OWNER)
    env = build_env(root, tmp_path, {"acme": enrichment_toml([d], BUILTINS + ["asn_owner"])})
    t0 = T0
    env.ingest("acme", [login("a1", "acme", t0, "alice@acme.test", US)])
    env.ingest("globex", [login("g1", "globex", t0, "gus@globex.test", US)])
    assert "asn_owner" in event_enrichment(env, "acme", "a1")
    assert "asn_owner" not in event_enrichment(env, "globex", "g1")


@pytest.mark.stretch
def test_plugins_can_depend_on_other_plugins(root, tmp_path):
    d = plugin_dir(tmp_path, asn_owner=ASN_OWNER, risk_tag=RISK_TAG)
    enabled = ["risk_tag", "asn_owner"] + BUILTINS  # dependent listed first
    env = build_env(root, tmp_path, {"acme": enrichment_toml([d], enabled)})
    env.ingest("acme", [login("e1", "acme", T0, "alice@acme.test", US)])
    assert event_enrichment(env, "acme", "e1")["risk_tag"]["tag"] == "tagged:AS64500-corp"


@pytest.mark.stretch
def test_several_plugin_directories_are_all_scanned(root, tmp_path):
    d1 = plugin_dir(tmp_path, "p1", asn_owner=ASN_OWNER)
    d2 = plugin_dir(tmp_path, "p2", risk_tag=RISK_TAG)
    env = build_env(root, tmp_path, {"acme": enrichment_toml([d1, d2], BUILTINS + ["asn_owner", "risk_tag"])})
    env.ingest("acme", [login("e1", "acme", T0, "alice@acme.test", US)])
    enr = event_enrichment(env, "acme", "e1")
    assert "asn_owner" in enr and "risk_tag" in enr
