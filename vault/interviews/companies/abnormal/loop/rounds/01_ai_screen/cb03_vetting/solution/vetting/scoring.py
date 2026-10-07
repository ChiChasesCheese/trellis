"""Findings -> score -> Recommendation. Thresholds come from the tenant's settings."""
from __future__ import annotations

from dataclasses import dataclass, replace

from vetting.models import Finding, Recommendation
from vetting.settings import Settings

MAX_SCORE = 100
CLEARED_NOTE = "previously cleared by reviewer"


@dataclass(frozen=True)
class ReviewerHistory:
    """Finding subjects (``asn:...``, ``phone:...``) this tenant's reviewers decided on."""

    cleared: frozenset[str] = frozenset()
    escalated: frozenset[str] = frozenset()


def apply_reviewer_history(findings: list[Finding], history: ReviewerHistory, settings: Settings) -> list[Finding]:
    """Soften one weak finding on a value a reviewer cleared. The finding and its evidence stay.

    Deliberately narrow so cleared values cannot launder an attacker: it applies only when that
    finding is the *only* one, is not heavy, and nobody escalated the same value.
    """
    if len(findings) != 1:
        return findings
    (finding,) = findings
    cfg = settings.feedback
    if (
        not finding.subject
        or finding.weight > cfg.weak_signal_max_weight
        or finding.subject not in history.cleared
        or finding.subject in history.escalated
    ):
        return findings
    softened = int(finding.weight * cfg.cleared_weight_factor)
    return [replace(finding, weight=softened, annotations=(*finding.annotations, CLEARED_NOTE))]


def score(findings: list[Finding], settings: Settings) -> tuple[int, Recommendation]:
    total = min(MAX_SCORE, sum(f.weight for f in findings))
    if total >= settings.highly_recommended_at:
        return total, Recommendation.HIGHLY_RECOMMENDED
    if total >= settings.recommended_at:
        return total, Recommendation.RECOMMENDED
    return total, Recommendation.NONE
