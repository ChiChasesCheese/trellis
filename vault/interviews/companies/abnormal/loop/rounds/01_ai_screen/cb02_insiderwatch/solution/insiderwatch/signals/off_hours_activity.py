"""Activity outside the user's local business hours (logins are ignored: people travel)."""
from __future__ import annotations

from typing import Iterable, Sequence

from ..events import Action, Event
from ..timeutil import is_business_hours, to_local
from .base import Finding, Signal, SignalContext, signal

_IGNORED = {Action.LOGIN, Action.LOGIN_FAILED}


@signal("off_hours_activity")
class OffHoursActivity(Signal):
    def evaluate(self, ctx: SignalContext, user: str, events: Sequence[Event]) -> Iterable[Finding]:
        cfg = ctx.config
        tz = ctx.roster.timezone_for(user, cfg.default_timezone)
        start, end = cfg.business_hours
        for ev in events:
            if ev.action in _IGNORED or is_business_hours(ev.ts, tz, start, end):
                continue
            local = to_local(ev.ts, tz)
            yield Finding(
                signal=self.name,
                user=user,
                ts=ev.ts,
                strength=0.5,
                reasons=(f"{ev.action.value} at {local:%a %H:%M} local time",),
                evidence={"action": ev.action.value, "target": ev.target},
            )
