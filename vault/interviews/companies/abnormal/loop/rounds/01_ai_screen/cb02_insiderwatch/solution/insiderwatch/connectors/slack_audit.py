"""Slack Enterprise audit logs. Timestamps are epoch seconds."""
from __future__ import annotations

from ..events import Action, Event
from ..timeutil import parse_ts
from .base import Connector, RawRecord, register_connector

_ACTIONS = {
    "file_downloaded": Action.FILE_DOWNLOAD,
    "user_login": Action.LOGIN,
    "workspace_export_started": Action.MESSAGE_EXPORT,
}


@register_connector
class SlackAuditConnector(Connector):
    source = "slack_audit"

    def parse_page(self, payload: dict) -> tuple[list[dict], str | None]:
        return payload["entries"], payload.get("response_metadata", {}).get("next_cursor") or None

    def normalize(self, raw: RawRecord) -> Event | None:
        rec = raw.payload
        action = _ACTIONS.get(rec.get("action", ""))
        if action is None:
            return self.drop("unmapped_action")
        email = rec.get("actor", {}).get("user", {}).get("email")
        if not email:
            return self.drop("no_user")
        entity = rec.get("entity", {})
        return Event(
            user=email,
            ts=parse_ts(rec["date_create"]),
            action=action,
            bytes=int(entity.get("size", 0)),
            target=entity.get("name", ""),
            source=self.source,
            attrs={"country": rec.get("context", {}).get("location", {}).get("country", "")}
            if action is Action.LOGIN else {},
        )
