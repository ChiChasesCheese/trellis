"""Findings -> score -> Recommendation. Thresholds come from the tenant's settings."""
from __future__ import annotations

from vetting.models import Finding, Recommendation
from vetting.settings import Settings

MAX_SCORE = 100


def score(findings: list[Finding], settings: Settings) -> tuple[int, Recommendation]:
    total = min(MAX_SCORE, sum(f.weight for f in findings))
    if total >= settings.highly_recommended_at:
        return total, Recommendation.HIGHLY_RECOMMENDED
    if total >= settings.recommended_at:
        return total, Recommendation.RECOMMENDED
    return total, Recommendation.NONE
