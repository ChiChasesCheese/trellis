"""Helpers for the cb04 acceptance tests.

Only entry points that exist in the starter are used: create_app(), the HTTP API through TestClient,
FakeMailbox, the injectable url_lookup, the ``quarantine.metrics`` counters and ``cli.main``.
"""
from __future__ import annotations

import io
import threading
import time
from pathlib import Path

TOKENS = {"acme": "tok-acme-analyst", "globex": "tok-globex-analyst"}
BAD_LINK = "https://login-micros0ft.example/verify"
FLAKY_LINK = "https://flaky-intel.example/ticket/1"  # the fixture URL intel raises LookupUnavailable for this host
CLEAN_SENDER = "Accounts <accounts@partner.example>"  # sender risk 10: nothing else pushes the verdict


def payload(
    message_id: str,
    reporter: str = "bob@acme.test",
    sender: str = CLEAN_SENDER,
    date: str = "Tue, 15 Sep 2026 08:00:00 +0000",
    links: tuple[str, ...] = (),
    attachments: tuple[dict, ...] = (),
    subject: str = "hello",
) -> dict:
    return {
        "message_id": message_id,
        "reporter": reporter,
        "headers": {"From": sender, "Date": date, "Subject": subject},
        "links": list(links),
        "attachments": list(attachments),
    }


class SlowLookup:
    """Wraps the real URL lookup and takes ``delay`` seconds: widens any check-then-act window."""

    def __init__(self, inner, delay: float):
        self.inner, self.delay = inner, delay

    def check(self, url: str):
        time.sleep(self.delay)
        return self.inner.check(url)


class BrokenLookup:
    """An intel provider that fails with something other than our own error type."""

    def check(self, url: str):
        raise RuntimeError("intel provider exploded")


class Env:
    def __init__(self, app, db_path: Path | None):
        self.app, self.db_path = app, db_path

    @property
    def mailbox(self):
        return self.app.mailbox

    def client(self, tenant: str):
        from quarantine.api.testing import TestClient

        return TestClient(self.app.wsgi, token=TOKENS[tenant])

    def post(self, tenant: str, body: dict):
        return self.client(tenant).post("/reports", body)

    def get(self, tenant: str, report_id: str):
        return self.client(tenant).get(f"/reports/{report_id}")

    def listing(self, tenant: str) -> dict:
        resp = self.client(tenant).get("/reports", params={"limit": 200})
        assert resp.status_code == 200, resp.json
        return resp.json

    def post_concurrently(self, tenant: str, bodies: list[dict]) -> list:
        """POST every body from its own thread, released together by a barrier."""
        barrier = threading.Barrier(len(bodies))
        results: list = [None] * len(bodies)

        def worker(i: int) -> None:
            client = self.client(tenant)
            barrier.wait()
            results[i] = client.post("/reports", bodies[i])

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(len(bodies))]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=30)
        return results

    def settle(self) -> None:
        """Run ``drain-outbox`` when the codebase has one (needs a file db); otherwise nothing to do."""
        if self.db_path is None:
            return
        from quarantine.cli import main

        try:
            main(["drain-outbox", "--db", str(self.db_path)], out=io.StringIO(), mailbox=self.mailbox)
        except SystemExit:
            pass  # no such command in this codebase


def build_env(tmp_path: Path, *, file_db: bool = False, mailbox=None, url_lookup=None, slow: float = 0.0) -> Env:
    """A fresh app (and fresh counters). ``slow`` wraps the real URL lookup with a delay."""
    from quarantine import metrics
    from quarantine.app import create_app
    from quarantine.config import FIXTURES_DIR
    from quarantine.lookups import FixtureUrlLookup

    metrics.reset()
    if slow and url_lookup is None:
        url_lookup = SlowLookup(FixtureUrlLookup(FIXTURES_DIR / "intel" / "urls.json"), slow)
    db_path = tmp_path / "q.db" if file_db else None
    app = create_app(db_path=db_path or ":memory:", mailbox=mailbox, url_lookup=url_lookup)
    return Env(app, db_path)
