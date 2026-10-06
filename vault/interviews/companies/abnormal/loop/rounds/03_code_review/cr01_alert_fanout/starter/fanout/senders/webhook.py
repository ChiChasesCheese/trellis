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
        log.info("POST %s headers=%s", channel.target, headers)
        try:
            with urllib.request.urlopen(req) as resp:
                if resp.status >= 300:
                    raise SendError(f"webhook returned {resp.status}")
        except urllib.error.URLError as exc:
            raise SendError(f"webhook failed: {exc}") from exc
