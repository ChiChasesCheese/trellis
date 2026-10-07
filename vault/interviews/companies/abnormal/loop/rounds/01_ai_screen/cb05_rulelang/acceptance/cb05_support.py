"""Helpers for the cb05 acceptance tests: build an app, feed it event rows, read signals back.

Only entry points that exist in the starter are used: create_app(), Pipeline.ingest_dir(), the events
jsonl format, GET /signals through TestClient, `python -m rulelang`, and tenant config files.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import textwrap
from datetime import datetime, timedelta, timezone
from pathlib import Path

TOKENS = {"acme": "tok-acme-analyst", "globex": "tok-globex-analyst"}
A = "acme.example"
T0 = datetime(2026, 9, 10, 9, 0, tzinfo=timezone.utc)  # the compromise time in the t3 scenario
BAD_LINK = "https://login-secure.evil-payments.example/pay"  # on the bad-host feed
YOUNG_DOMAIN = "fresh-supplier.example"  # registered 3 days ago
OLD_DOMAIN = "oldcorp.example"  # registered 4000 days ago


def stamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def email(event_id: str, tenant: str, ts: datetime, frm: str, to: list[str], subject: str = "hello", links=()) -> dict:
    return {"id": event_id, "tenant": tenant, "ts": stamp(ts), "kind": "email", "from": frm, "to": list(to),
            "subject": subject, "links": list(links)}


def tenant_toml(extra: str = "") -> str:
    """A tenant file that keeps acme's internal domain and adds ``extra`` (rules, detectors, blast_radius...)."""
    return f'[tenant]\ninternal_domains = ["{A}"]\n\n' + textwrap.dedent(extra)


class Env:
    def __init__(self, app, tmp_path: Path, config_dir: Path):
        self.app, self.tmp_path, self.config_dir, self._n = app, tmp_path, config_dir, 0

    def client(self, tenant: str):
        from rulelang.api.testing import TestClient

        return TestClient(self.app.wsgi, token=TOKENS[tenant])

    def write_events(self, *row_groups: list[dict]) -> Path:
        self._n += 1
        root = self.tmp_path / f"events{self._n}"
        root.mkdir()
        rows = [r for group in row_groups for r in group]
        (root / "events.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        return root

    def ingest(self, tenant: str, *row_groups: list[dict]):
        return self.app.pipeline.ingest_dir(self.write_events(*row_groups), tenant)

    def signals(self, tenant: str, event_id: str) -> list[dict]:
        resp = self.client(tenant).get("/signals", params={"event_id": event_id})
        assert resp.status_code == 200, resp.json
        return resp.json["items"]

    def detectors(self, tenant: str, event_id: str) -> set[str]:
        return {s["detector"] for s in self.signals(tenant, event_id)}


def make_config(root: Path, tmp_path: Path, tenant_files: dict[str, str] | None = None) -> Path:
    """A private copy of the config directory, with tenant files replaced."""
    cfg = tmp_path / "repo" / "config"
    shutil.copytree(root / "config", cfg)
    for tenant, toml in (tenant_files or {}).items():
        (cfg / "tenants" / f"{tenant}.toml").write_text(toml)
    return cfg


def build_env(root: Path, tmp_path: Path, tenant_files: dict[str, str] | None = None) -> Env:
    from rulelang.app import create_app

    cfg = make_config(root, tmp_path, tenant_files)
    return Env(create_app(config_dir=cfg, fixtures_dir=root / "fixtures"), tmp_path, cfg)


def run_cli(root: Path, *args: str) -> subprocess.CompletedProcess:
    """``python -m rulelang <args>`` in a subprocess, importing the codebase under test."""
    env = {**os.environ, "PYTHONPATH": str(root)}
    return subprocess.run([sys.executable, "-m", "rulelang", *args], cwd=root, env=env, capture_output=True,
                          text=True, timeout=60)


# ---------------------------------------------------------------- t3 scenario

def person(name: str) -> str:
    return f"{name}@{A}"


VENDOR = "vendor@acme-vendor.example"


def compromise_scenario(tenant: str = "acme") -> list[dict]:
    """dana is confirmed compromised at T0. Single-contact edges unless noted."""
    def mail(i, src, dst, minutes):
        return email(f"s{i:02d}", tenant, T0 + timedelta(minutes=minutes), src, [dst], "msg")

    return [
        mail(1, person("dana"), person("old"), -7200),     # long before the compromise
        mail(2, person("erin"), person("old2"), -1440),    # before the compromise
        mail(3, person("dana"), person("pat"), -7200),     # pat: one contact before ...
        mail(4, person("dana"), person("pat"), 90),        # ... and one after
        mail(5, person("ivy"), person("dana"), -60),       # incoming, not dana's doing
        mail(6, person("erin"), person("jon"), 30),        # after T0 but before erin heard from dana
        mail(7, person("dana"), person("erin"), 60),
        mail(8, person("dana"), VENDOR, 65),
        mail(9, person("erin"), person("frank"), 120),
        mail(10, person("erin"), person("gus"), 150),
        mail(11, person("frank"), person("hank"), 180),    # third hop
        mail(12, VENDOR, person("zoe"), 240),              # behind an external address
    ]
