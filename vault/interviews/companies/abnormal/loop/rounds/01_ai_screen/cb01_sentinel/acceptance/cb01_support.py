"""Helpers for the cb01 acceptance tests: build an app, feed it auth_log events, read alerts back.

Only entry points that exist in the starter are used: create_app(), Pipeline.ingest_dir(),
the auth_log jsonl format, the HTTP API through TestClient, and tenant config files.
"""
from __future__ import annotations

import json
import shutil
import textwrap
from datetime import datetime, timedelta, timezone
from pathlib import Path

TOKENS = {"acme": "tok-acme-analyst", "globex": "tok-globex-analyst"}
US, DE, SG = "198.51.100.7", "203.0.113.30", "198.18.5.5"
BOTNET_C2 = "203.0.113.250"
T0 = datetime(2026, 9, 1, 8, 0, tzinfo=timezone.utc)


def stamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def login(event_id: str, tenant: str, ts: datetime, user: str, ip: str, ok: bool = True) -> dict:
    return {
        "id": event_id, "tenant": tenant, "time": stamp(ts), "user": user, "ip": ip,
        "ua": "Mozilla/5.0 (acceptance)", "result": "success" if ok else "failure",
    }


def travel(tenant: str, user: str, via: str = DE, start: datetime = T0) -> list[dict]:
    """A US login and, 30 minutes later, a login from ``via`` (a different continent)."""
    return [
        login(f"{user}-us", tenant, start, user, US),
        login(f"{user}-via", tenant, start + timedelta(minutes=30), user, via),
    ]


def burst(tenant: str, user: str, ip: str, n: int, start: datetime = T0, prefix: str = "bf") -> list[dict]:
    """``n`` failed logins from one address, 15 seconds apart."""
    return [login(f"{prefix}-{user}-{i}", tenant, start + timedelta(seconds=15 * i), user, ip, ok=False) for i in range(n)]


class Env:
    def __init__(self, app, tmp_path: Path):
        self.app, self.tmp_path, self._n = app, tmp_path, 0

    def client(self, tenant: str):
        from sentinel.api.testing import TestClient

        return TestClient(self.app.wsgi, token=TOKENS[tenant])

    def ingest(self, tenant: str, *row_groups: list[dict]):
        """Write rows as an auth_log source directory and run the pipeline over it."""
        self._n += 1
        root = self.tmp_path / f"events{self._n}"
        (root / "auth_log").mkdir(parents=True)
        rows = [r for group in row_groups for r in group]
        (root / "auth_log" / "idp.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        return self.app.pipeline.ingest_dir(root, tenant)

    def alerts(self, tenant: str, status: str | None = "OPEN", rule: str | None = None) -> list[dict]:
        params = {"limit": 200}
        if status:
            params["status"] = status
        resp = self.client(tenant).get("/alerts", params=params)
        assert resp.status_code == 200, resp.json
        items = resp.json["items"]
        return [a for a in items if rule is None or rule in a["rule_ids"]]


def build_env(root: Path, tmp_path: Path, tenant_toml: dict[str, str] | None = None) -> Env:
    """An in-memory app whose config directory is a private copy, optionally with tenant overrides."""
    from sentinel.app import create_app

    cfg = tmp_path / "repo" / "config"
    shutil.copytree(root / "config", cfg)
    for tenant, toml in (tenant_toml or {}).items():
        (cfg / "tenants" / f"{tenant}.toml").write_text(textwrap.dedent(toml))
    app = create_app(config_dir=cfg, fixtures_dir=root / "fixtures")
    return Env(app, tmp_path)
