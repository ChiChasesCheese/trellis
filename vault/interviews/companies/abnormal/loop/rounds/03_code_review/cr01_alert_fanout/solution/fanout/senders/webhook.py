"""Webhook channel: POST the alert as JSON to the tenant's URL."""
from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request

from ..errors import SendError
from ..models import Alert, Channel

log = logging.getLogger(__name__)


class WebhookSender:
    def __init__(self, timeout_s: float = 5.0):
        self.timeout_s = timeout_s

    def send(self, channel: Channel, alert: Alert) -> None:
        payload = json.dumps(
            {
                "alert_id": alert.alert_id,
                "rule": alert.rule,
                "severity": alert.severity,
                "title": alert.title,
                "created_at": alert.created_at,
            }
        ).encode()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {channel.secret}",
        }
        req = urllib.request.Request(channel.target, data=payload, headers=headers, method="POST")
        log.info("POST %s (tenant=%s alert=%s)", channel.target, channel.tenant_id, alert.alert_id)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                if resp.status >= 300:
                    raise SendError(f"webhook returned {resp.status}")
        except (urllib.error.URLError, OSError) as exc:
            raise SendError(f"webhook failed: {exc}") from exc
