"""Receipts to the person who reported a message."""
from __future__ import annotations

from quarantine.actions.mailbox import Mailbox
from quarantine.models import Report


def send_receipt(mailbox: Mailbox, report: Report, to: str) -> None:
    """Send ``to`` the outcome for ``report``. Synchronous: the caller waits for the provider."""
    disposition = report.disposition.value if report.disposition else "UNKNOWN"
    mailbox.send_receipt(report.tenant_id, to, report.id, disposition)
