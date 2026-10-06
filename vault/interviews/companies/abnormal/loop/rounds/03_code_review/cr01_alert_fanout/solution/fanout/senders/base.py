from __future__ import annotations

from typing import Optional, Protocol

from ..models import Alert, Channel


class Sender(Protocol):
    def send(self, channel: Channel, alert: Alert) -> None:
        """Deliver `alert` through `channel`; raise SendError if it was not delivered."""


def format_message(alert: Alert, fields: Optional[list[str]] = None) -> str:
    fields = list(fields or [])
    if alert.user:
        fields.append(f"user={alert.user}")
    fields.append(f"severity={alert.severity}")
    return f"[{alert.rule}] {alert.title} ({', '.join(fields)})"
