from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    db_path: str = "fanout.db"
    queue_path: str = "queue.db"
    log_level: str = "INFO"
    # --- fan-out worker ---
    batch_size: int = 10
    visibility_timeout_s: int = 30
    concurrency: int = 8
    max_attempts: int = 3  # in-process attempts per channel per delivery
    max_receives: int = 5  # deliveries before a message is dead-lettered
    redelivery_base_s: float = 5.0  # visibility backoff after a failed delivery, doubled per receive
    retry_base_s: float = 0.2
    retry_cap_s: float = 5.0
    webhook_timeout_s: float = 5.0
    dedup_ttl_s: int = 3600
    max_alert_age_s: int = 900
    min_severity: int = 3
    poll_interval_s: float = 1.0

    @classmethod
    def from_env(cls) -> "Settings":
        s = cls()
        s.db_path = os.environ.get("FANOUT_DB", s.db_path)
        s.queue_path = os.environ.get("FANOUT_QUEUE", s.queue_path)
        s.log_level = os.environ.get("FANOUT_LOG_LEVEL", s.log_level)
        s.concurrency = int(os.environ.get("FANOUT_CONCURRENCY", s.concurrency))
        return s
