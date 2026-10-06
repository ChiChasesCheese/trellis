"""Shared builders for the fan-out acceptance tests. Only public entry points of the package are used."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from fanout.config_store import ConfigStore
from fanout.dedup import DedupCache
from fanout.models import Channel
from fanout.queue import Queue
from fanout.settings import Settings
from fanout.worker import Worker


class Clock:
    def __init__(self, t: float = 1_000_000.0):
        self.t = t

    def __call__(self) -> float:
        return self.t

    def advance(self, s: float) -> None:
        self.t += s


class Stop(BaseException):
    """Raised by a test sender to break out of an unbounded loop (BaseException: `except Exception` misses it)."""


class Crash(BaseException):
    """Simulates the process dying in the middle of a send."""


def alert_body(tenant="acme", alert_id="a1", rule="impossible_travel", severity=4, user="ann@example.com", age_s=5, created_at=None):
    if created_at is None:
        created_at = (datetime.now(timezone.utc) - timedelta(seconds=age_s)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return json.dumps(
        {"tenant_id": tenant, "alert_id": alert_id, "rule": rule, "severity": severity,
         "title": "Impossible travel", "user": user, "created_at": created_at}
    )


class Recorder:
    def __init__(self, observe=None):
        self.sent = []
        self.observe = observe

    def send(self, channel, alert):
        if self.observe:
            self.observe()
        self.sent.append((channel.tenant_id, channel.target, alert.alert_id))


class Failing:
    """Always raises SendError; after `limit` calls raises Stop so a hot loop cannot run forever."""

    def __init__(self, limit=50):
        self.calls = 0
        self.limit = limit

    def send(self, channel, alert):
        from fanout.errors import SendError

        self.calls += 1
        if self.calls >= self.limit:
            raise Stop()
        raise SendError("downstream 503")


class Rig:
    def __init__(self, channels, senders, store_cls=ConfigStore, **settings):
        self.clock = Clock()
        self.queue = Queue(clock=self.clock)
        self.dlq = Queue(clock=self.clock)
        self.store = store_cls()
        for ch in channels:
            self.store.add_channel(ch)
        self.sleeps = []
        self.worker = Worker(
            self.queue, self.store, DedupCache(clock=self.clock), senders,
            Settings(**{"concurrency": 4, **settings}), dlq=self.dlq, sleep=self.sleeps.append,
        )

    def close(self):
        self.worker.close()


def webhook(tenant="acme", target="https://hooks.example.com/acme", secret="s3cr3t-token"):
    return Channel(tenant, "webhook", target, secret=secret)
