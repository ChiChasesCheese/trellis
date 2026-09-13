"""q08 Store Closing-Time Penalty — reference solution.

Part 2 is a single O(n) pass: start with penalty(0) = number of 'Y' (all closed), then moving the
closing time one hour later turns that hour from closed to open: a 'Y' hour stops costing (-1),
an 'N' hour starts costing (+1). Part 3 is a small BEGIN/END state machine over whitespace tokens.
"""
from __future__ import annotations

import sys

HOURS = ("Y", "N")


def parse_log(log: str) -> list[str]:
    """Whitespace-separated tokens; a token like 'YYNY' counts as several hours."""
    return [ch for tok in log.split() for ch in tok]


def compute_penalty(log: str, closing_time: int) -> int:
    hours = parse_log(log)
    # open hours 1..closing_time (0-based [:closing_time]) with no customers, plus closed hours
    # closing_time+1..n with customers
    return hours[:closing_time].count("N") + hours[closing_time:].count("Y")


def find_best_closing_time(log: str) -> int:
    hours = parse_log(log)
    penalty = hours.count("Y")            # closing_time = 0: every customer-hour is missed
    best_time, best = 0, penalty
    for t, h in enumerate(hours, start=1):  # now hour t is open instead of closed
        penalty += 1 if h == "N" else -1
        if penalty < best:                  # strict '<' keeps the smallest time on a tie
            best_time, best = t, penalty
    return best_time


def get_best_closing_times(aggregate_log: str) -> list[int]:
    results: list[int] = []
    current: list[str] | None = None      # tokens of the open log, None = no BEGIN seen
    valid = True
    for tok in aggregate_log.split():
        if tok == "BEGIN":                # (re)start: an earlier unfinished log is discarded
            current, valid = [], True
        elif tok == "END":
            if current is not None and valid:
                results.append(find_best_closing_time(" ".join(current)))
            current = None                # END without BEGIN: nothing to close, ignored
        elif current is not None:
            if all(ch in HOURS for ch in tok):
                current.append(tok)
            else:
                valid = False             # garbage inside a log invalidates the whole log
        # tokens outside BEGIN...END are garbage and ignored
    return results


def part1(lines: list[str]) -> list[str]:
    out = []
    for ln in lines:
        log, _, t = ln.rpartition("|")
        out.append(str(compute_penalty(log, int(t))))
    return out


def part2(lines: list[str]) -> list[str]:
    return [str(find_best_closing_time(ln)) for ln in lines]


def part3(lines: list[str]) -> list[str]:
    return [str(t) for t in get_best_closing_times(" ".join(lines))]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    lines = [ln.strip() for ln in raw if ln.strip()]
    part = 3
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
