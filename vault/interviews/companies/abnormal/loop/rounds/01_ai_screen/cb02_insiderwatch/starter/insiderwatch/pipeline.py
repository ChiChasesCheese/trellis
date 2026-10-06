"""Replay pipeline: connectors -> events -> signals -> scoring -> alerts -> notifier.

Events are processed one UTC day at a time, in order. Signals for a day see baselines built from
earlier days only; the baseline is updated after the day is evaluated. Progress is kept in the
`replay_state` table, so replaying to a later `--until` only processes the new days.
"""
from __future__ import annotations

import logging
import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from .alerts import Alert, AlertStore
from .baselines import BaselineStore
from .config import Config
from .connectors import Connector, registered_connectors
from .events import Event, day_end
from .hr import Roster
from .notify import Notifier
from .scoring import score_finding
from .signals import SignalContext, all_signals

log = logging.getLogger(__name__)
WATERMARK_KEY = "last_processed_day"


@dataclass
class ReplaySummary:
    events: int = 0
    days: int = 0
    alerts: int = 0
    by_source: Counter = field(default_factory=Counter)
    by_action: Counter = field(default_factory=Counter)
    dropped: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "events": self.events,
            "days": self.days,
            "alerts": self.alerts,
            "by_source": dict(self.by_source),
            "by_action": dict(self.by_action),
            "dropped": self.dropped,
        }


def build_connectors(raw_dir: Path, config: Config) -> list[Connector]:
    connectors = []
    for source, cls in registered_connectors().items():
        root = Path(raw_dir) / source
        if root.is_dir():
            connectors.append(cls(root, config))
        else:
            log.info("no raw data for %s under %s, skipping", source, raw_dir)
    return connectors


class Pipeline:
    def __init__(self, conn: sqlite3.Connection, config: Config, roster: Roster,
                 connectors: list[Connector], notifier: Notifier) -> None:
        self._conn = conn
        self._config = config
        self._roster = roster
        self._connectors = connectors
        self._notifier = notifier
        self._baselines = BaselineStore(conn, config)
        self._alerts = AlertStore(conn)
        self._signals = all_signals()

    def _watermark(self) -> date | None:
        row = self._conn.execute("SELECT value FROM replay_state WHERE key = ?", (WATERMARK_KEY,)).fetchone()
        return date.fromisoformat(row["value"]) if row else None

    def _set_watermark(self, day: date) -> None:
        with self._conn:
            self._conn.execute(
                "INSERT INTO replay_state (key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value", (WATERMARK_KEY, day.isoformat()))

    def run(self, until: date) -> ReplaySummary:
        summary = ReplaySummary()
        watermark = self._watermark()
        limit = day_end(until)
        events: list[Event] = []
        for connector in self._connectors:
            for ev in connector.events():
                if ev.ts <= limit and (watermark is None or ev.day > watermark):
                    events.append(ev)
        events.sort(key=Event.sort_key)

        by_day: dict[date, list[Event]] = defaultdict(list)
        for ev in events:
            by_day[ev.day].append(ev)
            summary.by_source[ev.source] += 1
            summary.by_action[ev.action.value] += 1
        summary.events = len(events)

        for day in sorted(by_day):
            summary.alerts += self._process_day(day, by_day[day])
            summary.days += 1
        if watermark is None or until > watermark:
            self._set_watermark(until)
        summary.dropped = {c.source: c.stats.dropped_total for c in self._connectors}
        return summary

    def _process_day(self, day: date, events: list[Event]) -> int:
        per_user: dict[str, list[Event]] = defaultdict(list)
        for ev in events:
            per_user[ev.user].append(ev)
        ctx = SignalContext(day=day, baselines=self._baselines, roster=self._roster, config=self._config)
        created = 0
        for user in sorted(per_user):
            findings = [f for sig in self._signals for f in sig.evaluate(ctx, user, per_user[user])]
            for finding in sorted(findings, key=lambda f: f.ts):
                score = score_finding(finding, self._config)
                if score < self._config.alert_threshold:
                    continue
                alert = self._alerts.add(Alert(user=user, signal=finding.signal, score=score, ts=finding.ts,
                                               reasons=list(finding.reasons), evidence=dict(finding.evidence)))
                self._notifier.notify(alert)
                created += 1
        if self._config.flag("legacy_dlp_rules"):
            from .legacy import dlp_rules

            for ev in events:
                dlp_rules.scan_event(ev)
        self._baselines.update(events)
        return created
