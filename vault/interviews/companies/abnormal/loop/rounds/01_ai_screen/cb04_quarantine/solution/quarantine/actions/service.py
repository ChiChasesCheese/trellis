"""Acting on a mailbox. Everything goes through here so the action log stays complete."""
from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import datetime

from quarantine import metrics
from quarantine.actions.mailbox import Mailbox
from quarantine.models import Report, ReportStatus
from quarantine.store import ActionLogRepository, ReportRepository
from quarantine.timeutil import utcnow

log = logging.getLogger(__name__)

_RELEASABLE = (ReportStatus.QUARANTINED, ReportStatus.NEEDS_REVIEW)


class ActionService:
    def __init__(
        self,
        mailbox: Mailbox,
        reports: ReportRepository,
        action_log: ActionLogRepository,
        clock: Callable[[], datetime] = utcnow,
    ):
        self.mailbox = mailbox
        self.reports = reports
        self.action_log = action_log
        self.clock = clock

    def quarantine(self, report: Report) -> None:
        self.mailbox.quarantine(report.tenant_id, report.message_id)
        self.action_log.record(report.tenant_id, report.id, "quarantine", self.clock())
        metrics.incr("action.quarantine", tenant=report.tenant_id)
        log.info("quarantined report %s", report.id)

    def release(self, report: Report) -> bool:
        """Put a message back in the mailboxes it was pulled from. Idempotent: only the caller
        that wins the status change touches the mailbox. Returns whether this call did."""
        if not self.reports.set_status_if(report.tenant_id, report.id, _RELEASABLE, ReportStatus.RELEASED):
            metrics.incr("action.release_noop", tenant=report.tenant_id)
            return False
        try:
            self.mailbox.release(report.tenant_id, report.message_id)
        except Exception:
            self.reports.set_status(report.tenant_id, report.id, report.status or ReportStatus.QUARANTINED)
            raise
        self.action_log.record(report.tenant_id, report.id, "release", self.clock())
        metrics.incr("action.release", tenant=report.tenant_id)
        log.info("released report %s", report.id)
        return True
