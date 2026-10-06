"""Turn raw behavioural signals into a risk score."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskResult:
    score: int
    level: str
    factors: list[dict]


def level_for(score: int) -> str:
    if score >= 70:
        return "high"
    if score >= 30:
        return "medium"
    return "low"


def compute_risk(signals: list[tuple[str, int, str]]) -> RiskResult:
    """`signals` are (kind, weight, observed_at). The score is the capped sum of weights."""
    total = min(100, sum(w for _, w, _ in signals))
    top = sorted(signals, key=lambda s: (-s[1], s[0]))[:5]
    return RiskResult(score=total, level=level_for(total), factors=[{"kind": k, "weight": w} for k, w, _ in top])
