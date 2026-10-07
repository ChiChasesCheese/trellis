import json
from datetime import datetime, timezone

import pytest

from fanout import metrics
from fanout.config_store import ConfigStore
from fanout.dedup import DedupCache
from fanout.models import Channel
from fanout.queue import Queue
from fanout.settings import Settings
from fanout.worker import Worker


class Recorder:
    def __init__(self):
        self.sent = []

    def send(self, channel, alert):
        self.sent.append((channel.tenant_id, channel.target, alert.alert_id))


def alert_body(tenant="acme", alert_id="a1", rule="impossible_travel", severity=4, user="ann@example.com", age_s=5):
    created = datetime.fromtimestamp(datetime.now(timezone.utc).timestamp() - age_s, timezone.utc)
    return json.dumps(
        {
            "tenant_id": tenant,
            "alert_id": alert_id,
            "rule": rule,
            "severity": severity,
            "title": "Impossible travel",
            "user": user,
            "created_at": created.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    )


@pytest.fixture(autouse=True)
def _reset_metrics():
    metrics.reset()


@pytest.fixture
def rig():
    store = ConfigStore()
    store.add_channel(Channel("acme", "webhook", "https://hooks.example.com/acme", secret="s3cr3t"))
    store.add_channel(Channel("acme", "email", "secops@example.com"))
    rec = {"webhook": Recorder(), "email": Recorder()}
    queue = Queue()
    worker = Worker(queue, store, DedupCache(), rec, Settings(concurrency=2), dlq=Queue(), sleep=lambda s: None)
    yield queue, store, rec, worker
    worker.close()
