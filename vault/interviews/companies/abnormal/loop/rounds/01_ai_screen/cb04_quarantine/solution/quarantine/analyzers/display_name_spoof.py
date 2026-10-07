from __future__ import annotations

from quarantine.analyzers.base import AnalysisContext, Analyzer, register_analyzer
from quarantine.models import Report, Verdict


@register_analyzer
class DisplayNameSpoof(Analyzer):
    """A protected person's name, or an address of ours, shown on a message from outside."""

    name = "display_name_spoof"

    def analyze(self, report: Report, ctx: AnalysisContext) -> Verdict:
        settings = ctx.tenant(report)
        domain = report.sender.rpartition("@")[2]
        if domain in settings.domains:
            return Verdict(self.name, 0, ())
        shown = report.display_name.strip().casefold()
        if shown in {n.casefold() for n in settings.display_name.protected}:
            return Verdict(self.name, 80, (f"display name {report.display_name!r} sent from {domain}",))
        if "@" in shown and shown.rpartition("@")[2] in settings.domains:
            return Verdict(self.name, 70, (f"display name shows an internal address, sent from {domain}",))
        return Verdict(self.name, 0, ())
