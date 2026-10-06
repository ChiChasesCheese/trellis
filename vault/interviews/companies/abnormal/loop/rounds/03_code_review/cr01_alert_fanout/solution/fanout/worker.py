"""Notification fan-out worker.

Pulls high-severity alerts off the queue, looks up the tenant's channels, and sends each channel a
notification. Sends run on a thread pool so one slow tenant endpoint does not stall the batch.

Delivery contract: a message is deleted only after every channel either delivered or was already
delivered (at-least-once, made idempotent per channel by the dedup claim). Failures back off through
the queue's visibility timeout; after `max_receives` deliveries the message is dead-lettered.
"""
from __future__ import annotations

import json
import logging
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Callable, Mapping, Optional

from . import metrics
from .config_store import ConfigStore
from .dedup import DedupCache
from .errors import SendError
from .models import Alert, Channel, MalformedAlert
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
        self.dlq = dlq
        self.sleep = sleep
        self.pool = ThreadPoolExecutor(max_workers=self.settings.concurrency)

    def run_once(self) -> int:
        """Receive one batch and process it; returns the number of messages received."""
        msgs = self.queue.receive(self.settings.batch_size, self.settings.visibility_timeout_s)
        channel_cache: dict[str, list[Channel]] = {}
        cache_lock = threading.Lock()
        futures = [self.pool.submit(self.process_message, m, channel_cache, cache_lock) for m in msgs]
        for fut in futures:
            try:
                fut.result()
            except Exception:
                # Not acked: the message becomes visible again after the visibility timeout.
                log.exception("worker error")
        return len(msgs)

    def run_forever(self, stop: threading.Event) -> None:
        while not stop.is_set():
            if self.run_once() == 0:
                self.sleep(self.settings.poll_interval_s)

    def close(self) -> None:
        self.pool.shutdown(wait=True)

    # -- one message -----------------------------------------------------------------------------

    def process_message(
        self,
        msg: Message,
        channel_cache: Optional[dict[str, list[Channel]]] = None,
        cache_lock: Optional[threading.Lock] = None,
    ) -> None:
        try:
            alert = Alert.from_json(msg.body)
        except MalformedAlert as exc:
            self._dead_letter(msg, f"malformed: {exc}")
            return

        if alert.severity < self.settings.min_severity:
            metrics.inc("fanout.below_threshold")
            self.queue.delete(msg.receipt)
            return
        if self._age_s(alert) > self.settings.max_alert_age_s:
            log.info("alert %s is stale, skipping", alert.alert_id)
            metrics.inc("fanout.stale")
            self.queue.delete(msg.receipt)
            return

        failed = False
        for ch in self._channels(alert.tenant_id, channel_cache, cache_lock):
            sender = self.senders.get(ch.kind)
            if alert.severity < ch.min_severity or sender is None:
                continue
            # One claim per (alert, channel): redelivery after a partial failure only retries what failed.
            key = f"{alert.dedup_key}:{ch.kind}:{ch.target}"
            if not self.dedup.claim(key):
                metrics.inc("fanout.duplicate")
                continue
            delivered = False
            try:
                self._send_with_retry(sender, ch, alert)
                delivered = True
            except SendError as exc:
                failed = True
                log.warning("send to %s failed for alert %s: %s", ch.kind, alert.alert_id, exc)
            finally:
                if not delivered:
                    self.dedup.release(key)

        if not failed:
            self.queue.delete(msg.receipt)
        elif msg.receive_count >= self.settings.max_receives:
            self._dead_letter(msg, "max receives exceeded")
        else:
            delay = min(300.0, self.settings.redelivery_base_s * 2 ** (msg.receive_count - 1))
            self.queue.change_visibility(msg.receipt, delay)

    # -- helpers ---------------------------------------------------------------------------------

    @staticmethod
    def _age_s(alert: Alert) -> float:
        created = datetime.fromisoformat(alert.created_at.replace("Z", "+00:00"))
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - created).total_seconds()

    def _channels(self, tenant_id, cache, lock) -> list[Channel]:
        if cache is None or lock is None:
            return self.store.channels_for(tenant_id)
        with lock:  # one lookup per tenant per batch
            if tenant_id not in cache:
                cache[tenant_id] = self.store.channels_for(tenant_id)
            return cache[tenant_id]

    def _send_with_retry(self, sender: Sender, ch: Channel, alert: Alert) -> None:
        s = self.settings
        for attempt in range(1, s.max_attempts + 1):
            try:
                sender.send(ch, alert)
                metrics.inc(f"fanout.sent.{ch.kind}")
                return
            except SendError:
                metrics.inc(f"fanout.failed.{ch.kind}")
                if attempt == s.max_attempts:
                    raise
                backoff = min(s.retry_cap_s, s.retry_base_s * 2 ** (attempt - 1))
                self.sleep(backoff * random.uniform(0.5, 1.0))  # jitter: do not retry in lockstep

    def _dead_letter(self, msg: Message, reason: str) -> None:
        log.error("dead-lettering message %s: %s", msg.id, reason)
        metrics.inc("fanout.dead_lettered")
        if self.dlq is not None:
            self.dlq.send(json.dumps({"reason": reason, "receive_count": msg.receive_count, "body": msg.body}))
        self.queue.delete(msg.receipt)
