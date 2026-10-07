"""Intake: dedupe by (tenant, message id), analyse, decide, act, acknowledge."""
from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from quarantine import metrics
from quarantine.actions import ActionService, Mailbox, send_receipt
from quarantine.analyzers import AnalyzerRunner
from quarantine.config import SettingsProvider
from quarantine.decision import decide
from quarantine.intake.parsing import parse_report
from quarantine.models import Disposition, Report, status_for
from quarantine.store import ReportRepository
from quarantine.timeutil import utcnow

log = logging.getLogger(__name__)


@dataclass
class IntakeResult:
    report: Report
    created: bool  # False when the message had already been reported


class IntakeService:
    def __init__(
        self,
        settings: SettingsProvider,
        reports: ReportRepository,
        runner: AnalyzerRunner,
        actions: ActionService,
        mailbox: Mailbox,
        clock: Callable[[], datetime] = utcnow,
    ):
        self.settings = settings
        self.reports = reports
        self.runner = runner
        self.actions = actions
        self.mailbox = mailbox
        self.clock = clock

    def submit(self, tenant_id: str, payload: dict[str, Any]) -> IntakeResult:
        report = parse_report(payload, tenant_id, self.clock())
        log.info(
            "report received message_id=%s reporter=%s sender=%s",
            report.message_id, report.reporter, report.sender,
        )
        existing = self.reports.find_by_message(tenant_id, report.message_id)
        if existing is not None:
            return self._repeat(existing, report.reporter)
        decision = self.settings.for_tenant(tenant_id).decision
        report.verdicts = self.runner.run(report)
        report.disposition = decide(report.verdicts, decision)
        report.status = status_for(report.disposition)
        self.reports.insert(report)
        if report.disposition is Disposition.QUARANTINE:
            self.actions.quarantine(report)
        send_receipt(self.mailbox, report, to=report.reporter)
        metrics.incr("intake.created", tenant=tenant_id)
        return IntakeResult(report, created=True)

    def _repeat(self, existing: Report, reporter: str) -> IntakeResult:
        """Another person reported a message we know. Each report is fresh evidence: look again."""
        metrics.incr("intake.repeat", tenant=existing.tenant_id)
        decision = self.settings.for_tenant(existing.tenant_id).decision
        verdicts = self.runner.run(existing)
        disposition = decide(verdicts, decision)
        if disposition != existing.disposition:
            self.reports.update_outcome(
                existing.tenant_id, existing.id, verdicts, disposition, status_for(disposition)
            )
            existing.verdicts, existing.disposition = verdicts, disposition
            existing.status = status_for(disposition)
            if disposition is Disposition.QUARANTINE:
                self.actions.quarantine(existing)
        send_receipt(self.mailbox, existing, to=reporter)
        return IntakeResult(existing, created=False)
