"""q39 Server Uptime Log — reference solution.

'1' = crashed (down), '0' = up. Part 2 is one O(n) slide: penalty(0) = number of '0' (all hours
after removal); moving remove_at one hour later puts that hour on the network: a '0' stops costing
(-1), a '1' starts costing (+1). Part 3 is a BEGIN/END token state machine. Part 4 is a DP over
(hours, off-intervals used, on/off).
"""
from __future__ import annotations

import sys


def parse_log(log: str) -> list[str]:
    return [ch for tok in log.split() for ch in tok]


def compute_penalty(log: str, remove_at: int) -> int:
    hours = parse_log(log)
    # DOWN hours while on the network (hours 1..remove_at) + UP hours after removal
    return hours[:remove_at].count("1") + hours[remove_at:].count("0")


def find_best_removal_time(log: str) -> int:
    hours = parse_log(log)
    penalty = hours.count("0")             # remove_at = 0: every up hour is wasted
    best_time, best = 0, penalty
    for t, h in enumerate(hours, start=1):  # hour t is now on the network
        penalty += 1 if h == "1" else -1
        if penalty < best:                  # strict '<' keeps the smallest remove_at on a tie
            best_time, best = t, penalty
    return best_time


def get_best_removal_times(aggregate_log: str) -> list[int]:
    results: list[int] = []
    current: list[str] | None = None        # tokens since the last BEGIN; None = no open log
    for tok in aggregate_log.split():
        if tok == "BEGIN":                  # (re)start: an unfinished earlier log is discarded
            current = []
        elif tok == "END":
            if current is not None:
                results.append(find_best_removal_time(" ".join(current)))
            current = None                  # END without BEGIN: ignored
        elif current is not None and tok in ("0", "1"):
            current.append(tok)             # anything outside BEGIN...END is ignored
    return results


def min_penalty_k(log: str, k: int) -> int:
    hours = parse_log(log)
    INF = float("inf")
    on = [0] + [INF] * k                   # on[j]  = min penalty so far, j off-intervals used, on network now
    off = [INF] * (k + 1)                  # off[j] = ... currently off the network
    for h in hours:
        cost_on, cost_off = (1 if h == "1" else 0), (1 if h == "0" else 0)
        new_on = [min(on[j], off[j]) + cost_on for j in range(k + 1)]           # re-attach is free
        new_off = [min(off[j], on[j - 1] if j else INF) + cost_off for j in range(k + 1)]  # removal uses one
        on, off = new_on, new_off
    return int(min(min(on), min(off)))


def part1(lines: list[str]) -> list[str]:
    return [str(compute_penalty(log, int(t))) for log, _, t in (ln.rpartition("|") for ln in lines)]


def part2(lines: list[str]) -> list[str]:
    return [str(find_best_removal_time(ln)) for ln in lines]


def part3(lines: list[str]) -> list[str]:
    return [str(t) for t in get_best_removal_times(" ".join(lines))]


def part4(lines: list[str]) -> list[str]:
    return [str(min_penalty_k(log, int(k))) for log, _, k in (ln.rpartition("|") for ln in lines)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
