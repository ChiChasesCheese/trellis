"""Notification fan-out worker.

Pulls high-severity alerts off the queue, looks up the tenant's channels, and sends each channel a
notification. Sends run on a thread pool so one slow tenant endpoint does not stall the batch.
"""
from __future__ import annotations

import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Callable, Mapping, Optional

from . import metrics
from .config_store import ConfigStore
from .dedup import DedupCache
from .errors import SendError
from .models import Alert, MalformedAlert
from .queue import Message, Queue
from .senders import Sender
from .settings import Settings

log = logging.getLogger(__name__)


class Worker:
    def __init__(
        self,
        queue: Queue,
        store: ConfigStore,
        dedup: DedupCache,
        senders: Mapping[str, Sender],
        settings: Optional[Settings] = None,
        dlq: Optional[Queue] = None,
        sleep: Callable[[float], None] = time.sleep,
    ):
        self.queue = queue
        self.store = store
        self.dedup = dedup
        self.senders = dict(senders)
        self.settings = settings or Settings()
        self.dlq = dlq  # TODO: dead-letter poison messages once ops has created the DLQ
        self.sleep = sleep
        self.pool = ThreadPoolExecutor(max_workers=self.settings.concurrency)

    def run_once(self) -> int:
        """Receive one batch and process it; returns the number of messages received."""
        msgs = self.queue.receive(self.settings.batch_size, self.settings.visibility_timeout_s)
        futures = []
        for msg in msgs:
            self.queue.delete(msg.receipt)  # ack so the message is not delivered to another worker
            futures.append(self.pool.submit(self.process_message, msg))
        for fut in futures:
            try:
                fut.result()
            except Exception:
                log.exception("worker error")
        return len(msgs)

    def run_forever(self, stop: threading.Event) -> None:
        while not stop.is_set():
            if self.run_once() == 0:
                self.sleep(self.settings.poll_interval_s)

    def close(self) -> None:
        self.pool.shutdown(wait=True)

    def process_message(self, msg: Message) -> None:
        try:
            alert = Alert.from_json(msg.body)
        except MalformedAlert as exc:
            log.error("dropping message %s: %s", msg.id, exc)
            metrics.inc("fanout.malformed")
            return

        if alert.severity < self.settings.min_severity:
            metrics.inc("fanout.below_threshold")
            return

        created = datetime.fromisoformat(alert.created_at.replace("Z", ""))
        age = (datetime.now() - created).total_seconds()
        if age > self.settings.max_alert_age_s:
            log.info("alert %s is stale (%.0fs old), skipping", alert.alert_id, age)
            metrics.inc("fanout.stale")
            return

        if self.dedup.seen(alert.dedup_key):
            log.info("alert %s already notified, skipping", alert.dedup_key)
            metrics.inc("fanout.duplicate")
            return

        channels = self.store.channels_for(alert.tenant_id)
        for ch in channels:
            if alert.severity < ch.min_severity:
                continue
            sender = self.senders.get(ch.kind)
            if sender is None:
                log.warning("no sender for channel kind %r", ch.kind)
                continue
            attempt = 0
            while True:
                try:
                    sender.send(ch, alert)
                    metrics.inc(f"fanout.sent.{ch.kind}")
                    break
                except SendError as exc:
                    attempt += 1
                    log.warning("send to %s failed (attempt %d): %s", ch.kind, attempt, exc)
                    metrics.inc(f"fanout.failed.{ch.kind}")

        self.dedup.add(alert.dedup_key)
