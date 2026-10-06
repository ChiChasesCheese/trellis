"""Per-user, per-action rolling daily baselines, persisted in SQLite.

`get()` looks at the days strictly before `as_of`, so a day is never compared with itself. A
user's clock starts on their first recorded day of *any* activity; an action they never did
before is a real zero, not a missing baseline.
"""
from __future__ import annotations

import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable

from ..config import Config
from ..events import Action, Event
from ..timeutil import daterange
from . import stats


@dataclass(frozen=True)
class Baseline:
    user: str
    action: Action
    days_observed: int
    mean_count: float
    std_count: float
    p95_count: float
    mean_bytes: float
    std_bytes: float
    p95_bytes: float


class BaselineStore:
    def __init__(self, conn: sqlite3.Connection, config: Config) -> None:
        self._conn = conn
        self._config = config

    def update(self, events: Iterable[Event]) -> None:
        """Fold events into the daily totals. Safe to call once per replayed day."""
        totals: dict[tuple[str, str, str], list[int]] = defaultdict(lambda: [0, 0])
        first_day: dict[str, str] = {}
        countries: set[tuple[str, str, str]] = set()
        for ev in events:
            day = ev.day.isoformat()
            slot = totals[(ev.user, ev.action.value, day)]
            slot[0] += 1
            slot[1] += ev.bytes
            first_day[ev.user] = min(day, first_day.get(ev.user, day))
            country = ev.attrs.get("country")
            if ev.action is Action.LOGIN and country:
                countries.add((ev.user, country, day))
        with self._conn:
            for (user, action, day), (count, nbytes) in totals.items():
                self._conn.execute(
                    "INSERT INTO daily_totals (user, action, day, count, total_bytes) VALUES (?,?,?,?,?) "
                    "ON CONFLICT(user, action, day) DO UPDATE SET count = count + excluded.count, "
                    "total_bytes = total_bytes + excluded.total_bytes",
                    (user, action, day, count, nbytes),
                )
            for user, day in first_day.items():
                self._conn.execute(
                    "INSERT INTO user_activity (user, first_day) VALUES (?, ?) "
                    "ON CONFLICT(user) DO UPDATE SET first_day = MIN(first_day, excluded.first_day)",
                    (user, day),
                )
            for user, country, day in countries:
                self._conn.execute(
                    "INSERT OR IGNORE INTO login_countries (user, country, first_seen) VALUES (?,?,?)",
                    (user, country, day),
                )

    def get(self, user: str, action: Action, as_of: date) -> Baseline | None:
        """Baseline of `user`'s daily `action` activity before `as_of`; None during cold start."""
        row = self._conn.execute("SELECT first_day FROM user_activity WHERE user = ?", (user,)).fetchone()
        if row is None:
            return None
        start = max(date.fromisoformat(row["first_day"]), as_of - timedelta(days=self._config.baseline_window_days))
        days = list(daterange(start, as_of))
        if len(days) < self._config.baseline_min_days:
            return None
        rows = self._conn.execute(
            "SELECT day, count, total_bytes FROM daily_totals WHERE user = ? AND action = ? AND day >= ? AND day < ?",
            (user, action.value, start.isoformat(), as_of.isoformat()),
        ).fetchall()
        by_day = {r["day"]: (r["count"], r["total_bytes"]) for r in rows}
        counts = [float(by_day.get(d.isoformat(), (0, 0))[0]) for d in days]
        sizes = [float(by_day.get(d.isoformat(), (0, 0))[1]) for d in days]
        return Baseline(
            user=user,
            action=action,
            days_observed=len(days),
            mean_count=stats.mean(counts),
            std_count=stats.pstdev(counts),
            p95_count=stats.percentile(counts, 0.95),
            mean_bytes=stats.mean(sizes),
            std_bytes=stats.pstdev(sizes),
            p95_bytes=stats.percentile(sizes, 0.95),
        )

    def known_countries(self, user: str) -> set[str]:
        rows = self._conn.execute("SELECT country FROM login_countries WHERE user = ?", (user,))
        return {r["country"] for r in rows}
