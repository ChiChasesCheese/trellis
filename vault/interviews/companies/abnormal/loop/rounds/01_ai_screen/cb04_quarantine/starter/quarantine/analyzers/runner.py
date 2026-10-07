from __future__ import annotations

from quarantine import metrics
from quarantine.analyzers.base import ANALYZERS, AnalysisContext
from quarantine.models import Report, Verdict


class AnalyzerRunner:
    """Runs every registered analyzer over a report, counting each run in ``analyzer.run``."""

    def __init__(self, ctx: AnalysisContext):
        self.ctx = ctx

    def run(self, report: Report) -> list[Verdict]:
        verdicts: list[Verdict] = []
        for name, cls in sorted(ANALYZERS.items()):
            metrics.incr("analyzer.run", analyzer=name)
            verdicts.append(cls().analyze(report, self.ctx))
        return verdicts
