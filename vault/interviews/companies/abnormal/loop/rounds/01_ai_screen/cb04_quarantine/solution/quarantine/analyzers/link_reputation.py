from __future__ import annotations

from quarantine.analyzers.base import AnalysisContext, Analyzer, register_analyzer
from quarantine.models import Report, Verdict


@register_analyzer
class LinkReputation(Analyzer):
    """The worst score among the message's links, per the URL intel lookup."""

    name = "link_reputation"

    def analyze(self, report: Report, ctx: AnalysisContext) -> Verdict:
        score, reasons = 0, []
        for url in report.links:
            intel = ctx.url_lookup.check(url)
            if intel.score:
                reasons.append(f"{intel.host} is {intel.category} (risk {intel.score})")
            score = max(score, intel.score)
        return Verdict(self.name, score, tuple(reasons))
