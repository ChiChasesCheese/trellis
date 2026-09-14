"""pc23 Min Coins with Change -- reference solution.

You owe `n` units. You may hand over any amount P >= n made of coins from a denomination
set (unlimited supply of each), and receive back exact change C = P - n, also made of coins
from the same set. Minimise the TOTAL number of coins that change hands (paid + change).

Key fact used by every part: `min_coins(x, denoms)` -- the minimum coins needed to make exactly
x -- is computed by a plain unbounded-coin-change DP, never by greedy: greedy is only optimal for
"canonical" denomination sets, and Part 2's arbitrary sets are explicitly not canonical (e.g.
{1, 3, 4}: greedy makes 6 as 4+1+1 = 3 coins, optimal is 3+3 = 2 coins).

Bound on how far to search P: naively P could be unbounded. We only search
P in [n, n + WINDOW] where WINDOW = max(denoms) for the fixed canonical set (Part 1) and
2*max(denoms) for an arbitrary set (Part 2). This is an EMPIRICAL bound, not a worst-case proof:
- dp(x) is subadditive (dp(a+b) <= dp(a)+dp(b): concatenate optimal decompositions of a and b) but
  it is NOT monotonic in x even for simple sets (e.g. {1,5}: dp(4)=4 > dp(5)=1), so a clean
  exchange-argument proof that "the optimum always lands within one max-denomination of n" does not
  generalise to arbitrary sets.
- We verified computationally (see problem.md) that for the canonical set {1,5,10,50,100,200},
  widening the window from max(denoms) to 5*max(denoms) changes the answer for ZERO values of n
  in [0, 10000]; for the non-canonical {1,3,4} set, widening from max(denoms) (or 2*max(denoms))
  to 5*max(denoms) changes nothing for n in [0, 2000] either.
- Given that, the tests additionally cross-check the shipped window against a much larger window
  on randomised (n, denoms) inputs, so any future denomination set that broke the bound would be
  caught rather than silently accepted.
"""

from __future__ import annotations

import sys

CANONICAL_DENOMINATIONS: tuple[int, ...] = (1, 5, 10, 50, 100, 200)

INF = float("inf")

# dp arrays are expensive to rebuild (O(size * |denoms|)); a real interview would just use one
# fixed n, but this drill's line-driven main() answers thousands of queries against the same
# denomination set, so we cache the dp array per (sorted, deduped) denomination set and only
# EXTEND it when a bigger amount is asked for -- never recompute from scratch. The cache key is
# always the ascending-sorted set (order doesn't change the dp *values*, only how a reconstruction
# walks them), so Part 1/2/3 share one cache per denomination set regardless of which order each
# caller iterates coins in for its own purposes (e.g. Part 3 unwinds largest-first).
_DP_CACHE: dict[tuple[int, ...], list[float]] = {}


def _dp_key(denominations) -> tuple[int, ...]:
    return tuple(sorted(set(denominations)))


def _get_dp(denominations, size: int) -> list[float]:
    key = _dp_key(denominations)
    dp = _DP_CACHE.get(key)
    if dp is None:
        dp = [0.0]
        _DP_CACHE[key] = dp
    if len(dp) <= size:
        old_len = len(dp)
        dp.extend([INF] * (size + 1 - old_len))
        for x in range(old_len, size + 1):
            best = INF
            for d in key:
                if d <= x and dp[x - d] + 1 < best:
                    best = dp[x - d] + 1
            dp[x] = best
    return dp


def min_coins(x: int, denominations: tuple[int, ...] = CANONICAL_DENOMINATIONS) -> int:
    """Minimum coins to make exactly x >= 0 from `denominations` (unlimited supply each).
    Raises ValueError if x cannot be made (e.g. denominations has no coin of value 1 and x is
    not a combination of the coins present), or if x < 0."""
    if x < 0:
        raise ValueError(f"x must be >= 0, got {x!r}")
    dp = _get_dp(denominations, x)
    if dp[x] == INF:
        raise ValueError(f"{x} cannot be made from denominations {denominations}")
    return int(dp[x])


def _window(denominations: tuple[int, ...], multiplier: int) -> int:
    return multiplier * max(denominations)


def _min_total(n: int, denominations: tuple[int, ...], multiplier: int) -> int:
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n!r}")
    window = _window(denominations, multiplier)
    dp = _get_dp(denominations, n + window)
    best = INF
    for w in range(0, window + 1):
        paid = n + w
        if dp[paid] == INF or dp[w] == INF:
            continue
        best = min(best, dp[paid] + dp[w])
    if best == INF:
        raise ValueError(f"{n} is unreachable with denominations {denominations}")
    return int(best)


# --------------------------------------------------------------------------- Part 1
def min_total_coins_fixed(n: int) -> int:
    """Part1: canonical denominations {1,5,10,50,100,200}, n up to 1e4. Window = max(denoms)."""
    return _min_total(n, CANONICAL_DENOMINATIONS, multiplier=1)


# --------------------------------------------------------------------------- Part 2
def min_total_coins_custom(n: int, denominations: list[int]) -> int:
    """Part2 (reconstructed): arbitrary denomination set (not necessarily canonical -- greedy
    would be wrong). Window = 2*max(denoms) for extra safety margin over an unfamiliar set."""
    if not denominations or any(d <= 0 for d in denominations):
        raise ValueError(f"denominations must be non-empty positive integers, got {denominations!r}")
    denoms = tuple(sorted(set(denominations)))
    return _min_total(n, denoms, multiplier=2)


# --------------------------------------------------------------------------- Part 3
def min_total_coins_breakdown(
    n: int, denominations: tuple[int, ...] | list[int] = CANONICAL_DENOMINATIONS
) -> tuple[list[int], list[int]]:
    """Part3 (reconstructed): return ONE optimal (paid_coins, change_coins) breakdown, each a
    list of coin values (descending). sum(paid) - sum(change) == n and
    len(paid) + len(change) == min_total_coins for these denominations. Reconstruction is
    deterministic: ties in the DP are broken by preferring the largest denomination first, both
    when choosing the split point and when unwinding each amount into coins."""
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n!r}")
    denoms = tuple(sorted(set(denominations), reverse=True))
    if any(d <= 0 for d in denoms):
        raise ValueError(f"denominations must be positive, got {denominations!r}")
    multiplier = 1 if denoms == tuple(sorted(CANONICAL_DENOMINATIONS, reverse=True)) else 2
    window = _window(denoms, multiplier)
    dp = _get_dp(denoms, n + window)

    best_total, best_w = INF, 0
    for w in range(0, window + 1):
        paid = n + w
        if dp[paid] == INF or dp[w] == INF:
            continue
        total = dp[paid] + dp[w]
        if total < best_total:
            best_total, best_w = total, w
    if best_total == INF:
        raise ValueError(f"{n} is unreachable with denominations {denominations}")

    def _unwind(x: int) -> list[int]:
        coins: list[int] = []
        while x > 0:
            for d in denoms:  # largest first -> deterministic
                if d <= x and dp[x - d] == dp[x] - 1:
                    coins.append(d)
                    x -= d
                    break
            else:  # pragma: no cover -- dp is consistent by construction
                raise AssertionError("dp table inconsistent during reconstruction")
        return coins

    paid_amount = n + best_w
    return _unwind(paid_amount), _unwind(best_w)


def is_valid_optimal_breakdown(
    n: int, paid: list[int], change: list[int], denominations: tuple[int, ...] | list[int] = CANONICAL_DENOMINATIONS
) -> bool:
    """Checker used by tests: every coin is a valid denomination, the amounts are consistent
    with n, and the total coin count matches the true optimum."""
    denoms = tuple(sorted(set(denominations)))
    if any(c not in denoms for c in paid) or any(c not in denoms for c in change):
        return False
    if sum(paid) - sum(change) != n:
        return False
    optimal = min_total_coins_custom(n, list(denoms)) if denoms != CANONICAL_DENOMINATIONS else min_total_coins_fixed(n)
    return len(paid) + len(change) == optimal


# --------------------------------------------------------------------------- line-driven wrappers
def _read_n_lines(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    return lines[idx : idx + n], idx + n


def part1(lines: list[str]) -> list[str]:
    """'N k' / k integers -> k lines of min total coins (canonical denominations)."""
    queries, _ = _read_n_lines(lines, 0)
    return [str(min_total_coins_fixed(int(x))) for x in queries]


def part2(lines: list[str]) -> list[str]:
    """'D d1 d2 ...' / 'N k' / k integers -> k lines of min total coins for the given set."""
    tag, *denoms = lines[0].split()
    if tag != "D":
        raise ValueError(f"expected 'D d1 d2 ...', got {lines[0]!r}")
    denominations = [int(d) for d in denoms]
    queries, _ = _read_n_lines(lines, 1)
    return [str(min_total_coins_custom(int(x), denominations)) for x in queries]


def part3(lines: list[str]) -> list[str]:
    """'D d1 d2 ...' / 'N k' / k integers -> for each: 'paid|change', each side a comma-joined,
    descending list of coins, or '-' if that side is empty (paying exact change: n itself, or the
    degenerate n=0)."""
    tag, *denoms = lines[0].split()
    if tag != "D":
        raise ValueError(f"expected 'D d1 d2 ...', got {lines[0]!r}")
    denominations = [int(d) for d in denoms]
    queries, _ = _read_n_lines(lines, 1)
    out = []
    for x in queries:
        paid, change = min_total_coins_breakdown(int(x), denominations)
        p = ",".join(map(str, paid)) if paid else "-"
        c = ",".join(map(str, change)) if change else "-"
        out.append(f"{p}|{c}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
