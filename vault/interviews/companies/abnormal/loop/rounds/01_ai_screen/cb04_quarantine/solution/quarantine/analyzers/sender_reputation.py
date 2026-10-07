from __future__ import annotations

from datetime import timedelta

from quarantine.analyzers.base import AnalysisContext, Analyzer, register_analyzer
from quarantine.models import Report, Verdict


@register_analyzer
class SenderReputation(Analyzer):
    """Domain intel, plus a bonus when the same sender was reported again within the window."""

    name = "sender_reputation"

    def analyze(self, report: Report, ctx: AnalysisContext) -> Verdict:
        cfg = ctx.tenant(report).sender
        domain = report.sender.rpartition("@")[2]
        known = ctx.sender_intel.score(domain)
        reasons: list[str] = []
        if known is None:
            score = cfg.unknown_score
            reasons.append(f"no intel on sender domain {domain}")
        else:
            score = known
            reasons.append(f"sender domain {domain} has reputation risk {known}")
        earlier = ctx.reports.count_sender_reports(
            report.tenant_id,
            report.sender,
            since=report.sent_at - timedelta(hours=cfg.repeat_window_hours),
            until=report.sent_at,
            exclude_message_id=report.message_id,
        )
        if earlier:
            score += min(cfg.repeat_cap, cfg.repeat_bonus * earlier)
            reasons.append(f"{earlier} earlier report(s) from this sender in {cfg.repeat_window_hours}h")
        return Verdict(self.name, min(score, 100), tuple(reasons))
