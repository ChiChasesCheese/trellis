"""Drive the codebase only through its existing entry points: the CLI and the HTTP API."""
from __future__ import annotations

import json
from pathlib import Path

TOKENS = {"acme": "tok-acme-reviewer", "globex": "tok-globex-reviewer"}
RANK = {"NONE": 0, "RECOMMENDED": 1, "HIGHLY_RECOMMENDED": 2}


def gh_record(app_id, first, last, phone, ip, *, country="US", email=None, digest=None, author=None,
              tool="Example Word 16.0", resume_name=None, ua="FixtureBrowser/1.0"):
    """A Greenhouse application (the format `fixtures/greenhouse/applications/*.json` already uses)."""
    full = f"{first} {last}"
    email = email or f"{first}.{last}.{app_id}@example.com".lower()
    return {
        "id": app_id,
        "applied_at": "2026-09-20T12:00:00Z",
        "candidate": {
            "first_name": first,
            "last_name": last,
            "email_addresses": [{"value": email}],
            "phone_numbers": [{"value": phone}],
            "location": {"country": country},
        },
        "submission": {"ip_address": ip, "user_agent": ua},
        "attachments": [{
            "type": "resume",
            "metadata": {
                "author": author or full,
                "creator_tool": tool,
                "sha256": digest or f"{app_id:064x}",
                "extracted": {"name": resume_name or full, "email": email, "phone": phone},
            },
        }],
    }


class World:
    """One SQLite file, any number of tenants, ingest through the CLI, read through the API."""

    def __init__(self, tmp_path: Path) -> None:
        self.tmp = tmp_path
        self.db = tmp_path / "world.db"
        self._batches = 0

    def batch(self, records) -> Path:
        self._batches += 1
        root = self.tmp / f"batch{self._batches}"
        (root / "greenhouse" / "applications").mkdir(parents=True)
        (root / "greenhouse" / "applications" / "apps.json").write_text(json.dumps(records))
        return root

    def ingest(self, tenant: str, root: Path) -> int:
        from vetting.cli import main

        return main(["--db", str(self.db), "ingest", str(root), "--tenant", tenant])

    def ingest_records(self, tenant: str, records) -> None:
        assert self.ingest(tenant, self.batch(records)) == 0

    def client(self, tenant: str):
        from vetting.api.app import create_app
        from vetting.api.testing import TestClient

        return TestClient(create_app(self.db), token=TOKENS[tenant])

    def review(self, tenant: str, identity_id: str) -> dict:
        response = self.client(tenant).get(f"/reviews/{identity_id}")
        assert response.status == 200, response.json()
        return response.json()

    def level(self, tenant: str, identity_id: str) -> int:
        return RANK[self.review(tenant, identity_id)["recommendation"]]

    def by_name(self, tenant: str) -> dict[str, dict]:
        return {i["display_name"]: i for i in self.client(tenant).get("/reviews").json()["items"]}

    def decide(self, tenant: str, identity_id: str, decision: str, note: str = "") -> None:
        response = self.client(tenant).post(f"/reviews/{identity_id}/disposition", json={"decision": decision, "note": note})
        assert response.status in (200, 201), response.json()


def findings_text(detail: dict) -> str:
    return json.dumps(detail["findings"])


def signals(detail: dict) -> set[str]:
    return {f["signal"] for f in detail["findings"]}
