"""Turn the JSON the mail client posts into a ``Report``."""
from __future__ import annotations

import uuid
from datetime import datetime
from email.utils import parseaddr
from typing import Any

from quarantine.models import Attachment, Report
from quarantine.timeutil import parse_rfc2822


def new_report_id() -> str:
    return "rpt_" + uuid.uuid4().hex[:12]


def _sent_at(headers: dict[str, Any], fallback: datetime) -> datetime:
    """The message's own Date header, as a plain timestamp so reports compare easily."""
    parsed = parse_rfc2822(headers.get("Date"))
    if parsed is None:
        return fallback.replace(tzinfo=None)
    return parsed.replace(tzinfo=None)


def parse_report(payload: dict[str, Any], tenant_id: str, received_at: datetime) -> Report:
    headers = payload.get("headers", {})
    display_name, address = parseaddr(headers.get("From", ""))
    return Report(
        id=new_report_id(),
        tenant_id=tenant_id,
        message_id=payload["message_id"],
        reporter=payload["reporter"],
        sender=address.lower(),
        display_name=display_name,
        subject=headers.get("Subject", ""),
        sent_at=_sent_at(headers, received_at),
        received_at=received_at,
        links=[str(u) for u in payload.get("links", [])],
        attachments=[
            Attachment(a["filename"], a.get("content_type", "application/octet-stream"), a.get("size", 0))
            for a in payload.get("attachments", [])
        ],
    )
