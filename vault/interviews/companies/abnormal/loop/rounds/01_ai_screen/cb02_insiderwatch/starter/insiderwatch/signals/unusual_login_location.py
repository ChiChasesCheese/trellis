"""Login from a country the user has never signed in from before."""
from __future__ import annotations

from typing import Iterable, Sequence

from ..events import Action, Event
from .base import Finding, Signal, SignalContext, signal


@signal("unusual_login_location")
class UnusualLoginLocation(Signal):
    def evaluate(self, ctx: SignalContext, user: str, events: Sequence[Event]) -> Iterable[Finding]:
        if ctx.baselines.get(user, Action.LOGIN, ctx.day) is None:
            return  # cold start: every country would look new
        known = ctx.baselines.known_countries(user)
        reported: set[str] = set()
        for ev in events:
            country = ev.attrs.get("country")
            if ev.action is not Action.LOGIN or not country or country in known or country in reported:
                continue
            reported.add(country)
            yield Finding(
                signal=self.name,
                user=user,
                ts=ev.ts,
                strength=0.8,
                reasons=(f"first login from {country} (usual: {', '.join(sorted(known)) or 'none'})",),
                evidence={"country": country, "ip": ev.target},
            )
