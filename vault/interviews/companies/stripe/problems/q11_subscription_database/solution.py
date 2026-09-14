"""q11 Subscription Database — reference solution.

Per-user state is a single value: absent (not subscribed), None (unlimited) or an integer expiry
timestamp.  A check at time c is active iff the user is subscribed and (expiry is None or c <= expiry)
-- the boundary is INCLUSIVE (1,start,M,9 -> active at 10, inactive at 11).

Three modes share one simulate():
  "basic"      Part 1: no durations, every start is unlimited
  "replace"    Part 2: a new start overwrites the old subscription
  "accumulate" Part 3: a start on a still-active finite subscription extends it from its CURRENT expiry
Events are processed in input order (never re-sorted by timestamp).
"""
from __future__ import annotations

import sys

UNLIMITED = None


def parse(line: str) -> tuple[int, str, str, int | None]:
    parts = [p.strip() for p in line.split(",")]
    ts, op, user = int(parts[0]), parts[1].lower(), parts[2]
    dur = int(parts[3]) if len(parts) > 3 and parts[3] != "" else None
    return ts, op, user, dur


def is_active(expiry, t: int, subscribed: bool) -> bool:
    # inclusive: t == expiry is still active
    return subscribed and (expiry is UNLIMITED or t <= expiry)


def simulate(lines: list[str], mode: str) -> list[str]:
    subs: dict[str, int | None] = {}  # user -> expiry timestamp, or None for unlimited
    out: list[str] = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        t, op, user, dur = parse(raw)
        if op == "check":
            out.append("active" if is_active(subs.get(user), t, user in subs) else "inactive")
        elif op == "end":
            subs.pop(user, None)  # no-op if not subscribed
        elif op == "start":
            if mode == "basic":
                dur = None  # Part 1 ignores durations entirely
            new_expiry = UNLIMITED if dur is None else t + dur
            if mode == "accumulate" and user in subs and is_active(subs[user], t, True):
                cur = subs[user]
                if cur is UNLIMITED:
                    continue  # unlimited is never shortened or changed by a later start
                # extend from the CURRENT expiry, not from the new start's timestamp
                subs[user] = UNLIMITED if dur is None else cur + dur
            else:
                # Part 2 (replace), or Part 3 when the user is not currently active: fresh period
                subs[user] = new_expiry
        else:
            raise ValueError(f"unknown op {op!r}")
    return out


def part1(lines: list[str]) -> list[str]:
    return simulate(lines, "basic")


def part2(lines: list[str]) -> list[str]:
    return simulate(lines, "replace")


def part3(lines: list[str]) -> list[str]:
    return simulate(lines, "accumulate")


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 3
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
