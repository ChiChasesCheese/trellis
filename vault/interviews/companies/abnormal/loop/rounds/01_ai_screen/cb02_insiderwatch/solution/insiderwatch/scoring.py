"""Findings -> risk scores. Weights live in `Config.signal_weights`; decay is exponential."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Iterable

from .alerts.models import Alert
from .config import Config
from .signals import Finding

log = logging.getLogger(__name__)


def score_finding(finding: Finding, config: Config) -> float:
    weight = config.weight_for(finding.signal)
    if weight is None:
        log.warning("no weight configured for signal %s, using default %.2f", finding.signal,
                    config.default_signal_weight)
        weight = config.default_signal_weight
    return round(min(1.0, max(0.0, weight * finding.strength)), 4)


def severity_label(score: float, config: Config) -> str:
    if score >= config.severity_high:
        return "high"
    if score >= config.severity_medium:
        return "medium"
    return "low"


def decayed(score: float, ts: datetime, as_of: datetime, config: Config) -> float:
    age_days = max(0.0, (as_of - ts).total_seconds() / 86400)
    return score * 0.5 ** (age_days / config.score_half_life_days)


def user_risk(alerts: Iterable[Alert], as_of: datetime, config: Config) -> float:
    """Running risk for one user: sum of decayed alert scores."""
    return round(sum(decayed(a.score, a.ts, as_of, config) for a in alerts), 4)
