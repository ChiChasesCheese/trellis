"""`python -m fanout` runs the worker until interrupted."""
from __future__ import annotations

import logging
import threading

from .config_store import ConfigStore
from .dedup import DedupCache
from .queue import Queue
from .senders import EmailSender, SlackSender, WebhookSender
from .settings import Settings
from .worker import Worker


def build_worker(settings: Settings) -> Worker:
    return Worker(
        queue=Queue(settings.queue_path),
        dlq=Queue(settings.queue_path + ".dlq"),
        store=ConfigStore(settings.db_path),
        dedup=DedupCache(settings.dedup_ttl_s),
        senders={"webhook": WebhookSender(settings.webhook_timeout_s), "email": EmailSender(), "slack": SlackSender()},
        settings=settings,
    )


def main() -> None:
    settings = Settings.from_env()
    logging.basicConfig(level=settings.log_level)
    stop = threading.Event()
    worker = build_worker(settings)
    try:
        worker.run_forever(stop)
    except KeyboardInterrupt:
        stop.set()
    finally:
        worker.close()


if __name__ == "__main__":
    main()
