"""q41 Observability Metrics — reference solution.

RECONSTRUCTED TRAINING PROBLEM — see problem.md's warning block. Not a real Stripe question.

Four unlock-next-part levels over the same event shape (`timestamp,metric_name,labels,value`):
  Part 1: parse + aggregate by (metric_name, canonical_labels).
  Part 2: bucket into (possibly overlapping / sliding) time windows, with percentiles.
  Part 3: evaluate alerting rules over those windows with trigger/clear hysteresis.
  Part 4: process events in arrival order with a lateness watermark, dropping events too old,
          then run Part 3's exact rule evaluation over what's left.
"""

from __future__ import annotations

import math
import sys
from bisect import bisect_left
from typing import NamedTuple, Optional

STATS = ("count", "avg", "rate")
OPS = ("gt", "gte", "lt", "lte")


class Event(NamedTuple):
    timestamp: int
    metric: str
    labels: str  # already canonicalized
    value: float


class Rule(NamedTuple):
    metric: str
    labels: str
    stat: str
    op: str
    threshold: float
    trigger_n: int
    clear_n: int
    value_threshold: Optional[float]


# ------------------------------------------------------------------ formatting


def fmt2(x: float) -> str:
    """Two decimals, matching Python's f'{x:.2f}' rounding exactly (round-half-to-even on the
    underlying float) -- this is the pinned rule, not an independent decimal implementation."""
    return f"{x:.2f}"


# ------------------------------------------------------------------ parsing


def canonicalize_labels(raw: str) -> Optional[str]:
    """'-' -> '-'; 'b=2;a=1' -> 'a=1;b=2' (sorted by key). None on malformed input."""
    if raw == "-":
        return "-"
    if not raw:
        return None
    pairs = raw.split(";")
    parsed: list[tuple[str, str]] = []
    seen_keys: set[str] = set()
    for pair in pairs:
        if "=" not in pair:
            return None
        key, _, val = pair.partition("=")
        if not key or not val or key in seen_keys:
            return None
        seen_keys.add(key)
        parsed.append((key, val))
    parsed.sort(key=lambda kv: kv[0])
    return ";".join(f"{k}={v}" for k, v in parsed)


def parse_event_row(row: str) -> Optional[Event]:
    """One malformed-row check, one place -- returns None (never raises) on any format error."""
    fields = row.split(",")
    if len(fields) != 4:
        return None
    ts_raw, metric, labels_raw, value_raw = fields
    ts_raw, metric, labels_raw, value_raw = (
        ts_raw.strip(),
        metric.strip(),
        labels_raw.strip(),
        value_raw.strip(),
    )
    if not metric or not ts_raw.isdigit():
        return None
    try:
        value = float(value_raw)
    except ValueError:
        return None
    labels = canonicalize_labels(labels_raw)
    if labels is None:
        return None
    return Event(int(ts_raw), metric, labels, value)


def parse_events(rows: list[str]) -> tuple[list[Event], int]:
    """-> (well-formed events, malformed count)."""
    events, malformed = [], 0
    for row in rows:
        ev = parse_event_row(row)
        if ev is None:
            malformed += 1
        else:
            events.append(ev)
    return events, malformed


def parse_rule_row(row: str) -> Rule:
    """Rule rows are trusted config -- a malformed one is a fatal ValueError, not a skip."""
    fields = [p.strip() for p in row.split(",")]
    if len(fields) not in (7, 8):
        raise ValueError(f"malformed rule row: {row!r}")
    metric, labels_raw, stat, op, threshold_raw, trigger_raw, clear_raw = fields[:7]
    labels = canonicalize_labels(labels_raw)
    if labels is None:
        raise ValueError(f"malformed rule labels: {row!r}")
    if stat not in STATS:
        raise ValueError(f"unknown stat: {stat!r}")
    if op not in OPS:
        raise ValueError(f"unknown op: {op!r}")
    value_threshold = None
    if stat == "rate":
        if len(fields) != 8:
            raise ValueError(f"'rate' rule requires a value_threshold field: {row!r}")
        value_threshold = float(fields[7])
    elif len(fields) != 7:
        raise ValueError(f"only 'rate' rules take a value_threshold field: {row!r}")
    trigger_n, clear_n = int(trigger_raw), int(clear_raw)
    if trigger_n < 1 or clear_n < 1:
        raise ValueError(f"trigger_n/clear_n must be >= 1: {row!r}")
    return Rule(metric, labels, stat, op, float(threshold_raw), trigger_n, clear_n, value_threshold)


def _split(lines: list[str], markers: list[str]) -> dict[str, list[str]]:
    """Split lines into sections keyed by each marker in `markers` (in that fixed order); the
    final marker's rows run to the end of the input."""
    lines = [ln.strip() for ln in lines if ln.strip()]
    indices = []
    for marker in markers:
        if marker not in lines:
            raise ValueError(f"expected a {marker} section")
        indices.append(lines.index(marker))
    sections: dict[str, list[str]] = {}
    for i, marker in enumerate(markers):
        start = indices[i] + 1
        end = indices[i + 1] if i + 1 < len(indices) else len(lines)
        sections[marker] = lines[start:end]
    return sections


def _compare(value: float, op: str, threshold: float) -> bool:
    if op == "gt":
        return value > threshold
    if op == "gte":
        return value >= threshold
    if op == "lt":
        return value < threshold
    return value <= threshold  # lte


# ------------------------------------------------------------------ Part 1


def part1(lines: list[str]) -> list[str]:
    sections = _split(lines, ["EVENTS"])
    events, malformed = parse_events(sections["EVENTS"])
    groups: dict[tuple[str, str], list[float]] = {}
    for ev in events:
        groups.setdefault((ev.metric, ev.labels), []).append(ev.value)
    out = []
    for (metric, labels), values in sorted(groups.items()):
        count, total = len(values), sum(values)
        out.append(f"{metric},{labels} count={count} sum={fmt2(total)} avg={fmt2(total / count)}")
    out.append(f"MALFORMED {malformed}")
    return out


# ------------------------------------------------------------------ Part 2


def _series_index(events: list[Event]) -> dict[tuple[str, str], tuple[list[int], list[float]]]:
    """{(metric,labels): (sorted_timestamps, values_aligned_to_those_timestamps)}."""
    grouped: dict[tuple[str, str], list[tuple[int, float]]] = {}
    for ev in events:
        grouped.setdefault((ev.metric, ev.labels), []).append((ev.timestamp, ev.value))
    out = {}
    for key, pairs in grouped.items():
        pairs.sort(key=lambda tv: tv[0])
        out[key] = ([t for t, _ in pairs], [v for _, v in pairs])
    return out


def _window_values(ts: list[int], vals: list[float], size: int, step: int, k: int) -> list[float]:
    lo, hi = k * step, k * step + size
    i, j = bisect_left(ts, lo), bisect_left(ts, hi)
    return vals[i:j]


def _percentile(sorted_vals: list[float], p: int) -> float:
    """Nearest-rank: rank = ceil(p/100 * n), 1-indexed into the ascending-sorted values."""
    n = len(sorted_vals)
    rank = max(1, min(n, math.ceil(p / 100 * n)))
    return sorted_vals[rank - 1]


def _max_window_index(events: list[Event], step: int) -> int:
    if not events:
        return -1
    return max(ev.timestamp for ev in events) // step


def part2(lines: list[str]) -> list[str]:
    sections = _split(lines, ["WINDOW", "EVENTS"])
    size, step = (int(x) for x in sections["WINDOW"][0].split())
    events, malformed = parse_events(sections["EVENTS"])
    series = _series_index(events)
    max_k = _max_window_index(events, step)

    out_rows = []
    for (metric, labels), (ts, vals) in series.items():
        for k in range(max_k + 1):
            window_vals = _window_values(ts, vals, size, step, k)
            if not window_vals:
                continue
            count = len(window_vals)
            avg = sum(window_vals) / count
            sorted_vals = sorted(window_vals)
            p50, p90 = _percentile(sorted_vals, 50), _percentile(sorted_vals, 90)
            out_rows.append((metric, labels, k, count, avg, p50, p90))
    out_rows.sort(key=lambda r: (r[0], r[1], r[2]))
    out = [
        f"{metric},{labels},window={k} count={count} avg={fmt2(avg)} p50={fmt2(p50)} p90={fmt2(p90)}"
        for metric, labels, k, count, avg, p50, p90 in out_rows
    ]
    out.append(f"MALFORMED {malformed}")
    return out


# ------------------------------------------------------------------ Part 3


def _rule_stat_at_window(ts: list[int], vals: list[float], size: int, step: int, k: int, rule: Rule) -> float:
    window_vals = _window_values(ts, vals, size, step, k)
    if rule.stat == "count":
        return float(len(window_vals))
    if rule.stat == "avg":
        return sum(window_vals) / len(window_vals) if window_vals else 0.0
    # rate
    if not window_vals:
        return 0.0
    breaching = sum(1 for v in window_vals if v > rule.value_threshold)
    return breaching / len(window_vals)


def _evaluate_rules(
    rules: list[Rule],
    series: dict[tuple[str, str], tuple[list[int], list[float]]],
    size: int,
    step: int,
    max_k: int,
) -> list[str]:
    empty: tuple[list[int], list[float]] = ([], [])
    out = []
    for rule in rules:
        ts, vals = series.get((rule.metric, rule.labels), empty)
        state = "OK"
        consecutive_true = consecutive_false = 0
        for k in range(max_k + 1):
            stat_value = _rule_stat_at_window(ts, vals, size, step, k, rule)
            condition = _compare(stat_value, rule.op, rule.threshold)
            if condition:
                consecutive_true += 1
                consecutive_false = 0
            else:
                consecutive_false += 1
                consecutive_true = 0
            if state == "OK" and consecutive_true == rule.trigger_n:
                state = "FIRING"
                out.append(f"{rule.metric},{rule.labels} ALERT_ON window={k}")
                consecutive_true = 0
            elif state == "FIRING" and consecutive_false == rule.clear_n:
                state = "OK"
                out.append(f"{rule.metric},{rule.labels} ALERT_OFF window={k}")
                consecutive_false = 0
    return out


def part3(lines: list[str]) -> list[str]:
    sections = _split(lines, ["WINDOW", "RULES", "EVENTS"])
    size, step = (int(x) for x in sections["WINDOW"][0].split())
    rules = [parse_rule_row(r) for r in sections["RULES"]]
    events, malformed = parse_events(sections["EVENTS"])
    series = _series_index(events)
    max_k = _max_window_index(events, step)

    out = _evaluate_rules(rules, series, size, step, max_k)
    out.append(f"MALFORMED {malformed}")
    return out


# ------------------------------------------------------------------ Part 4


def part4(lines: list[str]) -> list[str]:
    sections = _split(lines, ["WINDOW", "RULES", "LATENESS", "EVENTS"])
    size, step = (int(x) for x in sections["WINDOW"][0].split())
    rules = [parse_rule_row(r) for r in sections["RULES"]]
    lateness = int(sections["LATENESS"][0])

    kept: list[Event] = []
    malformed = dropped = 0
    max_primary_seen = -1
    for row in sections["EVENTS"]:
        ev = parse_event_row(row)
        if ev is None:
            malformed += 1
            continue
        primary = ev.timestamp // step
        if primary < max_primary_seen - lateness:
            dropped += 1
            continue
        kept.append(ev)
        max_primary_seen = max(max_primary_seen, primary)

    series = _series_index(kept)
    max_k = _max_window_index(kept, step)
    out = _evaluate_rules(rules, series, size, step, max_k)
    out.append(f"DROPPED {dropped}")
    out.append(f"MALFORMED {malformed}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not raw:
        return
    part = int(raw[0].split()[1])
    fn = {1: part1, 2: part2, 3: part3, 4: part4}[part]
    out = fn(raw[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
