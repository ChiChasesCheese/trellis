"""Data leaving the building in the final days of employment, judged against the person's own baseline."""
from __future__ import annotations

from datetime import timedelta
from typing import Iterable, Sequence

from ..events import Action, Event
from .base import Finding, Signal, SignalContext, signal


@signal("departing_exfil")
class DepartingExfil(Signal):
    def evaluate(self, ctx: SignalContext, user: str, events: Sequence[Event]) -> Iterable[Finding]:
        cfg = ctx.config
        emp = ctx.roster.get(user)
        if emp is None:
            return
        last_day = emp.termination_date
        if last_day is None and emp.resignation_submitted is not None:
            last_day = emp.resignation_submitted + timedelta(days=cfg.departure_notice_days)
        if last_day is None:
            return

        if ctx.day > last_day:
            live = [e for e in events if e.action is not Action.LOGIN_FAILED]
            if live:
                yield Finding(
                    signal=self.name, user=user, ts=live[-1].ts, strength=1.0,
                    reasons=(f"{len(live)} events after last day {last_day.isoformat()}",),
                    evidence={"last_day": last_day.isoformat(), "events": len(live), "post_departure": True},
                )
            return
        if ctx.day < last_day - timedelta(days=cfg.departure_window_days):
            return

        exceeded: list[tuple[Action, str, Event]] = []
        for action in cfg.departing_exfil_actions:
            todays = [e for e in events if e.action is action]
            if not todays:
                continue
            baseline = ctx.baselines.get(user, action, ctx.day)
            total = sum(e.bytes for e in todays)
            if baseline is None:
                # cold start: egress to outside the company is suspicious on its own; bulk downloads are not
                if action is not Action.FILE_DOWNLOAD:
                    exceeded.append((action, f"{len(todays)}x {action.value} (no baseline yet)", todays[-1]))
                continue
            count_limit = max(baseline.p95_count * 1.25, baseline.p95_count + 0.5)
            over_count = len(todays) > count_limit
            over_bytes = total > 0 and total > baseline.p95_bytes * 1.25
            if over_count or over_bytes:
                exceeded.append((action, f"{len(todays)}x {action.value} ({total / 1e6:.0f} MB) vs usual "
                                         f"{baseline.mean_count:.1f}/day", todays[-1]))
        if not exceeded:
            return
        days_left = (last_day - ctx.day).days
        yield Finding(
            signal=self.name, user=user, ts=max(e.ts for _, _, e in exceeded),
            strength=min(1.0, 0.5 + 0.25 * (len(exceeded) - 1)),
            reasons=tuple(f"{reason}; {days_left}d before last day" for _, reason, _ in exceeded),
            evidence={"last_day": last_day.isoformat(), "actions": [a.value for a, _, _ in exceeded]},
        )
