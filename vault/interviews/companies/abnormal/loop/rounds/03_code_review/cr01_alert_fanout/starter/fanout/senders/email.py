"""Email channel. The SMTP client is stubbed behind `transport`."""
from __future__ import annotations

import logging
from typing import Callable

from ..models import Alert, Channel
from .base import format_message

log = logging.getLogger(__name__)


def _log_transport(to: str, subject: str, body: str) -> None:
    log.info("email stub: to=%s subject=%s", to, subject)


class EmailSender:
    def __init__(self, transport: Callable[[str, str, str], None] = _log_transport):
        self.transport = transport

    def send(self, channel: Channel, alert: Alert) -> None:
        try:
            self.transport(channel.target, f"Alert: {alert.title}", format_message(alert))
        except Exception:
            pass
