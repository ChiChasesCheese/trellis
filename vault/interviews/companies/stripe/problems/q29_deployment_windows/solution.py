"""q29 Deployment Windows — reference solution.

Everything is integer minutes. A region rule is (name, utc_offset_minutes, weekdays, start, end)
with `end > start` (a wrapping window has end += 1440). Business hours are half-open [start, end).
UTC = local - offset. For UTC day D we look at the region's local dates D-2..D+2 (offsets up to
+-14 h plus a wrapping 24 h window can spill that far), clip to [0, 1440), union, complement.
"""
from __future__ import annotations

import sys
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import NamedTuple

DAY = 1440
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
HORIZON_DAYS = 366  # Part 3 gives up after this many days


class Rule(NamedTuple):
    name: str
    offset: int              # minutes, local = UTC + offset
    days: frozenset[int]     # local weekdays (Mon=0) on which the rule applies
    start: int               # local minutes since local midnight
    end: int                 # > start; may exceed 1440 when the window wraps midnight


def hhmm(s: str) -> int:
    h, m = s.strip().split(":")
    return int(h) * 60 + int(m)


def parse_offset(s: str) -> int:
    return int(Decimal(s.strip()) * 60)  # "+5.5" -> 330, "-8" -> -480 (exact, no float)


def parse_days(s: str) -> frozenset[int]:
    out: set[int] = set()
    for chunk in s.split("/"):
        a, _, b = chunk.strip().partition("-")
        lo, hi = WEEKDAYS.index(a), WEEKDAYS.index(b or a)
        out.update(range(lo, hi + 1) if lo <= hi else list(range(lo, 7)) + list(range(0, hi + 1)))
    return frozenset(out)


def parse_rule(line: str) -> Rule:
    f = [p.strip() for p in line.split(",")]
    days = parse_days(f[2]) if len(f) == 5 else frozenset(range(7))
    start, end = hhmm(f[-2]), hhmm(f[-1])
    if end <= start:            # wrap past midnight; start == end means the whole day
        end += DAY
    return Rule(f[0], parse_offset(f[1]), days, start, end)


def split_rules(lines: list[str]) -> tuple[list[Rule], set[date]]:
    rules, blackout = [], set()
    for ln in lines:
        if ln.lower().startswith("blackout"):
            blackout.add(date.fromisoformat(ln.split(",")[1].strip()))
        elif ln.strip():
            rules.append(parse_rule(ln))
    return rules, blackout


def merge(iv: list[tuple[int, int]]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for s, e in sorted(iv):
        if out and s <= out[-1][1]:        # overlapping OR touching -> merge
            out[-1] = (out[-1][0], max(out[-1][1], e))
        else:
            out.append((s, e))
    return out


def free_windows(rules: list[Rule], day: date) -> list[tuple[int, int]]:
    """Minutes of UTC `day` during which no region is in business hours (complement of the union)."""
    busy = []
    for r in rules:
        for k in (-2, -1, 0, 1, 2):
            if (day + timedelta(days=k)).weekday() not in r.days:
                continue
            s, e = k * DAY + r.start - r.offset, k * DAY + r.end - r.offset
            s, e = max(s, 0), min(e, DAY)
            if s < e:
                busy.append((s, e))
    free, cur = [], 0
    for s, e in merge(busy):
        if s > cur:
            free.append((cur, s))
        cur = e
    if cur < DAY:
        free.append((cur, DAY))
    return free


def fmt_time(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}"          # 1440 -> "24:00"


def fmt_window(day: date, s: int, e: int) -> str:
    return f"{day.isoformat()}T{fmt_time(s)}..{fmt_time(e)}"


def scan(rules: list[Rule], blackout: set[date], now: datetime, min_len: int, k: int | None, horizon: int) -> list[str]:
    """Windows of length >= min_len, day by day from `now`, at most k, within `horizon` days."""
    out: list[str] = []
    cache: dict[int, list[tuple[int, int]]] = {}   # free windows depend only on the weekday
    now_min = now.hour * 60 + now.minute
    for i in range(horizon):
        if k is not None and len(out) >= k:
            break
        day = now.date() + timedelta(days=i)
        if day in blackout:
            continue
        wd = day.weekday()
        if wd not in cache:
            cache[wd] = free_windows(rules, day)
        for s, e in cache[wd]:
            if i == 0:
                s = max(s, now_min)              # first day: nothing before "now"
            if e - s >= min_len and (k is None or len(out) < k):   # >= : exactly L qualifies
                out.append(fmt_window(day, s, e))
    return out


def part1(lines: list[str]) -> list[str]:
    local_day = datetime.fromisoformat(lines[0].strip())
    out = []
    for r in (parse_rule(ln) for ln in lines[1:] if ln.strip()):
        s = local_day + timedelta(minutes=r.start - r.offset)
        e = local_day + timedelta(minutes=r.end - r.offset)
        out.append(f"{r.name} {s:%Y-%m-%dT%H:%M}..{e:%Y-%m-%dT%H:%M}")
    return out


def part2(lines: list[str]) -> list[str]:
    day = date.fromisoformat(lines[0].strip())
    rules, _ = split_rules(lines[1:])
    return [fmt_window(day, s, e) for s, e in free_windows(rules, day)]


def part3(lines: list[str]) -> list[str]:
    now_s, l_s, k_s = (p.strip() for p in lines[0].split(","))
    rules, blackout = split_rules(lines[1:])
    return scan(rules, blackout, datetime.fromisoformat(now_s), int(l_s), int(k_s), HORIZON_DAYS)


def part4(lines: list[str]) -> list[str]:
    day_s, l_s = (p.strip() for p in lines[0].split(","))
    rules, blackout = split_rules(lines[1:])
    return scan(rules, blackout, datetime.fromisoformat(day_s), int(l_s), None, 7)


def variant_week_intervals(rows: list[str]) -> list[list[int]]:
    """PracHub variant: allowed minus freeze over minutes-in-week [0, 10080), half-open, merged."""
    allowed, freeze = [], []
    for row in rows:
        s, e, typ = (p.strip() for p in row.split(","))
        (allowed if typ == "allowed" else freeze).append((int(s), int(e)))
    out = []
    for s, e in merge(allowed):
        cur = s
        for fs, fe in merge(freeze):
            if fe <= cur or fs >= e:
                continue
            if fs > cur:
                out.append([cur, fs])
            cur = max(cur, fe)
        if cur < e:
            out.append([cur, e])
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 3
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines) if lines else []
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
