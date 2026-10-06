"""Org-chart helpers over the roster."""
from __future__ import annotations

from .roster import Employee, Roster


def manager_chain(roster: Roster, user: str, max_depth: int = 10) -> list[Employee]:
    """Managers above `user`, nearest first. Stops on a cycle or a manager missing from the roster."""
    chain: list[Employee] = []
    seen = {user}
    current = roster.get(user)
    while current is not None and current.manager and current.manager not in seen and len(chain) < max_depth:
        seen.add(current.manager)
        current = roster.get(current.manager)
        if current is not None:
            chain.append(current)
    return chain


def direct_reports(roster: Roster, manager: str) -> list[Employee]:
    return sorted((e for e in roster if e.manager == manager), key=lambda e: e.email)
