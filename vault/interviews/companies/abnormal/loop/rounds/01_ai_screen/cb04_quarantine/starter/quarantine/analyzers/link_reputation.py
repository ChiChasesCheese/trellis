from __future__ import annotations

import logging

from quarantine.analyzers.base import AnalysisContext, Analyzer, register_analyzer
from quarantine.models import Report, Verdict

log = logging.getLogger(__name__)


@register_analyzer
class LinkReputation(Analyzer):
    """The worst score among the message's links, per the URL intel lookup."""

    name = "link_reputation"

    def analyze(self, report: Report, ctx: AnalysisContext) -> Verdict:
        score, reasons = 0, []
        for url in report.links:
            try:
                intel = ctx.url_lookup.check(url)
            except Exception:
                log.debug("url lookup failed for %s", url)
                return Verdict(self.name, 0, ())
            if intel.score:
                reasons.append(f"{intel.host} is {intel.category} (risk {intel.score})")
            score = max(score, intel.score)
        return Verdict(self.name, score, tuple(reasons))
