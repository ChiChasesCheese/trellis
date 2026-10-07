"""Intake: dedupe by (tenant, message id), analyse, decide, act, acknowledge."""
from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from quarantine import metrics
from quarantine.actions import ActionService, enqueue_receipt
from quarantine.analyzers import AnalyzerRunner
from quarantine.config import SettingsProvider
from quarantine.decision import decide
from quarantine.errors import DuplicateReport
from quarantine.intake.parsing import parse_report
from quarantine.models import Disposition, Report, status_for
from quarantine.store import OutboxRepository, ReportRepository
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
        outbox: OutboxRepository,
        clock: Callable[[], datetime] = utcnow,
    ):
        self.settings = settings
        self.reports = reports
        self.runner = runner
        self.actions = actions
        self.outbox = outbox
        self.clock = clock

    def submit(self, tenant_id: str, payload: dict[str, Any]) -> IntakeResult:
        cfg = self.settings.for_tenant(tenant_id)
        report = parse_report(payload, tenant_id, self.clock(), cfg.intake.max_links)
        log.info("report received id=%s tenant=%s", report.id, tenant_id)
        existing = self.reports.find_by_message(tenant_id, report.message_id)
        if existing is not None:
            return self._repeat(existing, report.reporter)
        report.verdicts = self.runner.run(report)
        report.disposition = decide(report.verdicts, cfg.decision)
        report.status = status_for(report.disposition)
        try:
            self.reports.insert(report)
        except DuplicateReport:
            # Lost a race with another report of the same message: join the winner's incident.
            existing = self.reports.find_by_message(tenant_id, report.message_id)
            assert existing is not None
            return self._repeat(existing, report.reporter)
        if report.disposition is Disposition.QUARANTINE:
            self.actions.quarantine(report)
        enqueue_receipt(self.outbox, report, to=report.reporter, at=self.clock())
        metrics.incr("intake.created", tenant=tenant_id)
        return IntakeResult(report, created=True)

    def _repeat(self, existing: Report, reporter: str) -> IntakeResult:
        """Another person reported a message we already analysed: record them, do not analyse again."""
        metrics.incr("intake.repeat", tenant=existing.tenant_id)
        now = self.clock()
        if self.reports.add_reporter(existing.tenant_id, existing.id, reporter, now):
            enqueue_receipt(self.outbox, existing, to=reporter, at=now)
        existing.reporter_count = self.reports.reporter_count(existing.tenant_id, existing.id)
        return IntakeResult(existing, created=False)
