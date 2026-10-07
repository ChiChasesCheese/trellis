"""Turn the JSON the mail client posts into a ``Report``."""
from __future__ import annotations

import uuid
from datetime import datetime
from email.utils import parseaddr
from typing import Any

from quarantine.errors import ValidationError
from quarantine.models import Attachment, Report
from quarantine.timeutil import parse_rfc2822, to_utc


def new_report_id() -> str:
    return "rpt_" + uuid.uuid4().hex[:12]


def _sent_at(headers: dict[str, Any], fallback: datetime) -> datetime:
    """The message's own Date header in UTC; the time we received the report when it has none."""
    parsed = parse_rfc2822(headers.get("Date"))
    return to_utc(parsed if parsed is not None else fallback)


def _text(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{key} is required and must be a non-empty string")
    return value.strip()


def _list(payload: dict[str, Any], key: str) -> list[Any]:
    value = payload.get(key, [])
    if not isinstance(value, list):
        raise ValidationError(f"{key} must be a list")
    return value


def _attachment(raw: Any) -> Attachment:
    if not isinstance(raw, dict) or not isinstance(raw.get("filename"), str) or not raw["filename"]:
        raise ValidationError("each attachment needs a filename")
    return Attachment(raw["filename"], raw.get("content_type", "application/octet-stream"), raw.get("size", 0))


def parse_report(
    payload: dict[str, Any], tenant_id: str, received_at: datetime, max_links: int = 50
) -> Report:
    headers = payload.get("headers", {})
    if not isinstance(headers, dict):
        raise ValidationError("headers must be an object")
    links = _list(payload, "links")
    if not all(isinstance(u, str) for u in links):
        raise ValidationError("links must be a list of strings")
    if len(links) > max_links:
        raise ValidationError(f"a report may carry at most {max_links} links")
    display_name, address = parseaddr(headers.get("From", ""))
    return Report(
        id=new_report_id(),
        tenant_id=tenant_id,
        message_id=_text(payload, "message_id"),
        reporter=_text(payload, "reporter"),
        sender=address.lower(),
        display_name=display_name,
        subject=headers.get("Subject", ""),
        sent_at=_sent_at(headers, received_at),
        received_at=received_at,
        links=links,
        attachments=[_attachment(a) for a in _list(payload, "attachments")],
    )
