"""q23 Work Schedule -- reference solution.

pattern is exactly 7 characters (one per day of the week), each either a literal digit '0'-'8'
(hours already fixed for that day) or '?' (hours to be decided, any integer in [0, dayHours]).
Find every way to replace the '?'s so the week's total equals workHours.

Part1: return every valid schedule (as a 7-character string), sorted lexicographically.
Backtracking over the '?' positions in left-to-right order with feasibility pruning (a partial
sum that can no longer reach workHours, given how many '?'s and how much fixed total remain, is
abandoned) -- visiting question-mark values in ascending order means solutions are already
generated in lexicographic order, so no separate sort is needed for a fixed pattern.

Part2 (reconstructed): count only (mod 1e9+7), pattern length up to 1e3 and workHours up to 1e4.
A DP over (day index, running total) would be O(n * S * dayHours) if done naively; using a
prefix-sum trick per day (each '?' contributes a sliding-window sum over the previous day's DP
row) drops that to O(n * S).
"""

from __future__ import annotations

import sys

MOD = 1_000_000_007
PATTERN_LEN = 7


def _validate(pattern: str, work_hours: int, day_hours: int) -> None:
    if len(pattern) != PATTERN_LEN:
        raise ValueError(f"pattern must be exactly {PATTERN_LEN} characters, got {len(pattern)}")
    for c in pattern:
        if c != "?" and c not in "012345678":
            raise ValueError(f"pattern characters must be '?' or a digit 0-8: {c!r}")
    if day_hours < 0 or day_hours > 8:
        raise ValueError(f"dayHours must be in [0, 8]: {day_hours}")
    if work_hours < 0:
        raise ValueError(f"workHours must be >= 0: {work_hours}")


# --------------------------------------------------------------------------- Part 1
def all_schedules(pattern: str, work_hours: int, day_hours: int) -> list[str]:
    """Every 7-character schedule matching pattern with digits summing to work_hours, sorted
    lexicographically."""
    _validate(pattern, work_hours, day_hours)
    n = len(pattern)
    chars = list(pattern)
    q_positions = [i for i, c in enumerate(pattern) if c == "?"]
    fixed_total = sum(int(c) for c in pattern if c != "?")
    # suffix_fixed[i] = sum of fixed digits at positions >= i (for pruning against upcoming fixed days)
    suffix_fixed = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_fixed[i] = suffix_fixed[i + 1] + (int(pattern[i]) if pattern[i] != "?" else 0)
    q_count_from = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        q_count_from[i] = q_count_from[i + 1] + (1 if pattern[i] == "?" else 0)

    results: list[str] = []

    def rec(i: int, running: int) -> None:
        if i == n:
            if running == work_hours:
                results.append("".join(chars))
            return
        remaining_fixed = suffix_fixed[i + 1] if chars[i] != "?" else suffix_fixed[i]
        # after processing position i, however it's set, the remaining budget must come from
        # later fixed digits + later '?'s (each in [0, day_hours])
        if pattern[i] != "?":
            new_running = running + int(pattern[i])
            lo = new_running + suffix_fixed[i + 1]
            hi = new_running + suffix_fixed[i + 1] + q_count_from[i + 1] * day_hours
            if lo <= work_hours <= hi:
                rec(i + 1, new_running)
            return
        for v in range(day_hours + 1):
            new_running = running + v
            lo = new_running + suffix_fixed[i + 1]
            hi = new_running + suffix_fixed[i + 1] + q_count_from[i + 1] * day_hours
            if lo > work_hours:
                break  # v only increases from here, lo only grows
            if hi < work_hours:
                continue
            chars[i] = str(v)
            rec(i + 1, new_running)
            chars[i] = "?"

    rec(0, 0)
    return results


# --------------------------------------------------------------------------- Part 2
def count_schedules_mod(pattern: str, work_hours: int, day_hours: int) -> int:
    """Number of valid schedules mod 1e9+7. pattern length up to 1e3, workHours up to 1e4.
    O(n * S) via prefix-sum sliding window per day."""
    if any(c != "?" and c not in "012345678" for c in pattern):
        raise ValueError("pattern characters must be '?' or a digit 0-8")
    if day_hours < 0 or day_hours > 8:
        raise ValueError(f"dayHours must be in [0, 8]: {day_hours}")
    if work_hours < 0:
        raise ValueError(f"workHours must be >= 0: {work_hours}")

    S = work_hours
    dp = [0] * (S + 1)
    dp[0] = 1
    for c in pattern:
        new_dp = [0] * (S + 1)
        if c != "?":
            d = int(c)
            for s in range(d, S + 1):
                new_dp[s] = dp[s - d]
        else:
            # new_dp[s] = sum(dp[s-v] for v in 0..day_hours if s-v >= 0), via prefix sums
            prefix = [0] * (S + 2)
            for s in range(S + 1):
                prefix[s + 1] = (prefix[s] + dp[s]) % MOD
            for s in range(S + 1):
                lo = max(0, s - day_hours)
                new_dp[s] = (prefix[s + 1] - prefix[lo]) % MOD
        dp = new_dp
    return dp[S] % MOD


# --------------------------------------------------------------------------- line-driven wrappers
def _read(lines: list[str]) -> tuple[str, int, int]:
    pattern = lines[0].strip()
    work_hours, day_hours = map(int, lines[1].split())
    return pattern, work_hours, day_hours


def part1(lines: list[str]) -> list[str]:
    """'pattern' / 'workHours dayHours' -> all valid schedules, sorted lexicographically."""
    pattern, work_hours, day_hours = _read(lines)
    return all_schedules(pattern, work_hours, day_hours)


def part2(lines: list[str]) -> list[str]:
    """same input -> [count mod 1e9+7]."""
    pattern, work_hours, day_hours = _read(lines)
    return [str(count_schedules_mod(pattern, work_hours, day_hours))]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
