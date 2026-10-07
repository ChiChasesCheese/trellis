from __future__ import annotations

import logging

from quarantine import metrics
from quarantine.analyzers.base import ANALYZERS, AnalysisContext
from quarantine.models import Report, Verdict

log = logging.getLogger(__name__)


class AnalyzerRunner:
    """Runs every registered analyzer over a report, counting each run in ``analyzer.run``.

    An analyzer that raises yields an inconclusive verdict instead of failing the report.
    """

    def __init__(self, ctx: AnalysisContext):
        self.ctx = ctx

    def run(self, report: Report) -> list[Verdict]:
        verdicts: list[Verdict] = []
        for name, cls in sorted(ANALYZERS.items()):
            metrics.incr("analyzer.run", analyzer=name)
            try:
                verdicts.append(cls().analyze(report, self.ctx))
            except Exception as exc:
                metrics.incr("analyzer.error", analyzer=name)
                log.warning("analyzer %s failed on report %s: %s", name, report.id, exc)
                verdicts.append(Verdict(name, 0, (f"{name} could not run",), inconclusive=True))
        return verdicts
