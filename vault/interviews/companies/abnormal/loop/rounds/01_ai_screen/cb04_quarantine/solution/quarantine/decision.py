"""Verdicts -> Disposition, using the tenant's thresholds."""
from __future__ import annotations

from collections.abc import Sequence

from quarantine.config import DecisionSettings
from quarantine.models import Disposition, Verdict


def decide(verdicts: Sequence[Verdict], settings: DecisionSettings) -> Disposition:
    """The highest single score wins: one strong signal is enough to act on.

    An analyzer that could not run never counts as a clean bill: the message goes to a human.
    """
    top = max((v.score for v in verdicts), default=0)
    if top >= settings.quarantine_at:
        return Disposition.QUARANTINE
    if top >= settings.review_at or any(v.inconclusive for v in verdicts):
        return Disposition.NEEDS_REVIEW
    return Disposition.RELEASE
