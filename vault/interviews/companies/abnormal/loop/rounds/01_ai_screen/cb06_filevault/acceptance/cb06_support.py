"""Helpers for the cb06 acceptance tests: build an app, upload through the API, count blobs on disk.

Only entry points that exist in the starter are used: ``create_app(data_dir, clock=, env=)``, the HTTP API
through ``TestClient`` (``X-User-Id``, JSON uploads with base64 content), ``filevault.metrics``, and the
``data_dir/blobs`` directory that ``LocalDiskStore`` writes to.
"""
from __future__ import annotations

import base64
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

T0 = datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc)


class Clock:
    def __init__(self, now: datetime = T0):
        self.now = now

    def __call__(self) -> datetime:
        return self.now

    def tick(self, **delta: float) -> None:
        self.now += timedelta(**delta)


class Env:
    def __init__(self, app, data_dir: Path, clock: Clock):
        self.app, self.data_dir, self.clock = app, data_dir, clock

    def client(self, user: str):
        from filevault.api.testing import TestClient

        return TestClient(self.app.wsgi, user=user)

    def upload(self, user: str, filename: str, data: bytes, content_type: str = "application/octet-stream"):
        return self.client(user).post(
            "/files",
            {"filename": filename, "content_type": content_type, "content_base64": base64.b64encode(data).decode()},
        )

    def upload_ok(self, user: str, filename: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        resp = self.upload(user, filename, data, content_type)
        assert resp.status_code == 201, resp.json
        return resp.json["id"]

    def listing(self, user: str, **params) -> list[dict]:
        resp = self.client(user).get("/files", params or None)
        assert resp.status_code == 200, resp.json
        return resp.json["items"]

    def names(self, user: str, **params) -> list[str]:
        return sorted(item["filename"] for item in self.listing(user, **params))

    def download(self, user: str, file_id: str) -> bytes | None:
        resp = self.client(user).get(f"/files/{file_id}/content")
        return resp.body if resp.status_code == 200 else None

    def blob_count(self) -> int:
        blobs = self.data_dir / "blobs"
        return sum(1 for p in blobs.rglob("*") if p.is_file() and not p.name.endswith(".part"))


def slow_local_store(root: Path, delay: float = 0.05):
    """A LocalDiskStore whose put/exists/delete take ``delay`` seconds.

    Widens every check-then-act window so a solution that is not atomic interleaves on every run
    instead of once in a while. A correct (transactional) solution just gets slower.
    """
    from filevault.storage import LocalDiskStore

    class SlowStore(LocalDiskStore):
        def put(self, path, data):
            time.sleep(delay)
            super().put(path, data)

        def exists(self, path):
            time.sleep(delay)
            return super().exists(path)

        def delete(self, path):
            time.sleep(delay)
            super().delete(path)

    return SlowStore(root)


def build_env(tmp_path: Path, slow_store: bool = False, **settings) -> Env:
    """``settings`` become ``FILEVAULT_*`` overrides, e.g. ``quota_bytes_per_user=1000``.

    ``slow_store=True`` injects a slow blob store through ``create_app(store=...)``.
    """
    from filevault.app import create_app

    clock = Clock()
    env = {f"FILEVAULT_{k.upper()}": str(v) for k, v in settings.items()}
    data_dir = tmp_path / "data"
    store = slow_local_store(data_dir / "blobs") if slow_store else None
    return Env(create_app(data_dir, store=store, clock=clock, env=env), data_dir, clock)


def run_together(*jobs) -> list[BaseException]:
    """Start each job in its own thread, release them through a barrier, return any exceptions."""
    barrier = threading.Barrier(len(jobs))
    errors: list[BaseException] = []

    def wrap(job):
        def run():
            try:
                barrier.wait(timeout=5)
                job()
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)

        return run

    threads = [threading.Thread(target=wrap(job)) for job in jobs]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=15)
    return errors
