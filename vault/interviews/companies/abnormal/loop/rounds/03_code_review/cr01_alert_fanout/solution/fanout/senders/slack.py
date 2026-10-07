"""Slack channel. The Slack API client is stubbed behind `transport`."""
from __future__ import annotations

import logging
from typing import Callable

from ..errors import SendError
from ..models import Alert, Channel
from .base import format_message

log = logging.getLogger(__name__)


def _log_transport(channel: str, text: str) -> None:
    log.info("slack stub: channel=%s text=%s", channel, text)


class SlackSender:
    def __init__(self, transport: Callable[[str, str], None] = _log_transport):
        self.transport = transport

    def send(self, channel: Channel, alert: Alert) -> None:
        try:
            self.transport(channel.target, format_message(alert))
        except Exception as exc:
            raise SendError(f"slack transport failed: {exc}") from exc
