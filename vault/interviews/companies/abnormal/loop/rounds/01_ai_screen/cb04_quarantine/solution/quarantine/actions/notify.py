"""Receipts to the person who reported a message: queued on intake, delivered by ``drain``."""
from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from quarantine import metrics
from quarantine.actions.mailbox import Mailbox
from quarantine.models import Report
from quarantine.store import OutboxRepository
from quarantine.timeutil import utcnow

log = logging.getLogger(__name__)


def enqueue_receipt(outbox: OutboxRepository, report: Report, to: str, at: datetime) -> None:
    """Queue a receipt for ``to``; nothing is sent until ``drain`` runs."""
    disposition = report.disposition.value if report.disposition else "UNKNOWN"
    outbox.enqueue(report.tenant_id, report.id, to, disposition, at)


@dataclass
class DrainResult:
    delivered: int = 0
    failed: int = 0


def drain(
    outbox: OutboxRepository,
    mailbox: Mailbox,
    tenant_id: str,
    limit: int = 500,
    clock: Callable[[], datetime] = utcnow,
) -> DrainResult:
    """Deliver a tenant's pending receipts, oldest first. Failures stay queued for the next run."""
    result = DrainResult()
    for item in outbox.pending(tenant_id, limit):
        try:
            mailbox.send_receipt(tenant_id, item.recipient, item.report_id, item.disposition)
        except Exception as exc:
            outbox.mark_failed(tenant_id, item.id, str(exc))
            metrics.incr("outbox.failed", tenant=tenant_id)
            log.warning("receipt %s not delivered (attempt %s)", item.id, item.attempts + 1)
            result.failed += 1
        else:
            outbox.mark_sent(tenant_id, item.id, clock())
            metrics.incr("outbox.delivered", tenant=tenant_id)
            result.delivered += 1
    return result
