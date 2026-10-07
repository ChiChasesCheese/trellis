from __future__ import annotations

from typing import TextIO

from ..alerts.models import Alert
from ..config import Config
from ..scoring import severity_label


def format_alert(alert: Alert, config: Config) -> str:
    severity = severity_label(alert.score, config).upper()
    return f"[{severity}] {alert.user} {alert.signal} score={alert.score:.2f}: {'; '.join(alert.reasons)}"


class ConsoleNotifier:
    def __init__(self, config: Config, stream: TextIO) -> None:
        self._config = config
        self._stream = stream

    def notify(self, alert: Alert) -> None:
        print(format_alert(alert, self._config), file=self._stream)
