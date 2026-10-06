"""Read-only reports over what replay has stored."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

from .alerts import Alert
from .config import Config
from .scoring import severity_label, user_risk


@dataclass(frozen=True)
class UserRisk:
    user: str
    risk: float
    alert_count: int
    top_signal: str
    severity: str
    last_alert: datetime


def risk_table(alerts: list[Alert], as_of: datetime, config: Config) -> list[UserRisk]:
    """One row per user with alerts, highest decayed risk first."""
    by_user: dict[str, list[Alert]] = defaultdict(list)
    for alert in alerts:
        by_user[alert.user].append(alert)
    rows = []
    for user, items in by_user.items():
        risk = user_risk(items, as_of, config)
        signal_scores: dict[str, float] = defaultdict(float)
        for item in items:
            signal_scores[item.signal] += item.score
        rows.append(UserRisk(
            user=user,
            risk=risk,
            alert_count=len(items),
            top_signal=max(signal_scores, key=signal_scores.__getitem__),
            severity=severity_label(max(a.score for a in items), config),
            last_alert=max(a.ts for a in items),
        ))
    return sorted(rows, key=lambda r: (-r.risk, r.user))


def render_risk_table(rows: list[UserRisk]) -> str:
    lines = [f"{'user':<30} {'risk':>6} {'alerts':>6}  {'worst':<7} top signal"]
    for row in rows:
        lines.append(f"{row.user:<30} {row.risk:>6.2f} {row.alert_count:>6}  {row.severity:<7} {row.top_signal}")
    return "\n".join(lines)
