"""q24 Maximum Throughput -- reference solution.

A pipeline of n services in series; its throughput is the MINIMUM across all services (the
bottleneck). Service i starts at throughput[i]. Each "upgrade" of service i costs a flat
scalingCost[i] and multiplies its capacity: after x upgrades, service i's capacity is
throughput[i] * (1 + x) -- this multiplicative formula is (reconstructed). Given a total budget
B, maximise the pipeline's (bottleneck) throughput.

Part1: binary search on the answer T. feasible(T) = can every service reach capacity >= T
within budget B? For service i, the minimal upgrade count is x_i = max(0, ceil(T / t_i) - 1),
costing x_i * scalingCost[i]; sum over i and compare to B. feasible() is monotonic in T (higher
T never gets cheaper), so binary search finds the maximal feasible T in O(n log(range)).

Part2 (reconstructed): return the actual per-service upgrade counts achieving the optimum (a
checker recomputes the achieved bottleneck and total cost from them). Because feasible(T) uses
the *minimal* cost per service independently, the plan for the binary-search-selected T* is
provably tight -- some service's capacity lands exactly on T* (proof: if every service
overshot T*, that same plan would already prove a higher T feasible too, contradicting T*'s
maximality), so the achieved bottleneck always equals T* exactly.
"""

from __future__ import annotations

import sys


def _validate(throughput: list[int], scaling_cost: list[int], budget: int) -> None:
    if not throughput:
        raise ValueError("throughput must be non-empty")
    if len(throughput) != len(scaling_cost):
        raise ValueError("throughput and scalingCost must be the same length")
    if budget < 0:
        raise ValueError("budget must be >= 0")
    for t in throughput:
        if t < 1:
            raise ValueError(f"throughput must be >= 1: {t}")
    for c in scaling_cost:
        if c < 1:
            raise ValueError(f"scalingCost must be >= 1: {c}")


def _upgrades_needed(t: int, target: int) -> int:
    """Minimal x >= 0 such that t * (1 + x) >= target."""
    if t >= target:
        return 0
    # ceil(target / t) - 1
    return -(-target // t) - 1


def _cost_for_target(throughput: list[int], scaling_cost: list[int], target: int, budget: int) -> tuple[bool, int]:
    total = 0
    for t, c in zip(throughput, scaling_cost):
        total += _upgrades_needed(t, target) * c
        if total > budget:
            return False, total
    return True, total


# --------------------------------------------------------------------------- Part 1
def max_min_throughput(throughput: list[int], scaling_cost: list[int], budget: int) -> int:
    """Maximum achievable bottleneck throughput within budget. O(n log(max_target))."""
    _validate(throughput, scaling_cost, budget)
    lo = min(throughput)
    # safe upper bound: spend the whole budget on the cheapest-to-upgrade service alone
    hi = max(t * (2 + budget) for t in throughput)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        feasible, _ = _cost_for_target(throughput, scaling_cost, mid, budget)
        if feasible:
            lo = mid
        else:
            hi = mid - 1
    return lo


# --------------------------------------------------------------------------- Part 2
def max_min_throughput_with_plan(
    throughput: list[int], scaling_cost: list[int], budget: int
) -> tuple[int, list[int]]:
    """(achieved bottleneck, per-service upgrade counts) achieving the optimum."""
    target = max_min_throughput(throughput, scaling_cost, budget)
    upgrades = [_upgrades_needed(t, target) for t in throughput]
    return target, upgrades


# --------------------------------------------------------------------------- line-driven wrappers
def _read(lines: list[str]) -> tuple[list[int], list[int], int]:
    n, budget = map(int, lines[0].split())
    throughput = list(map(int, lines[1].split())) if n else []
    scaling_cost = list(map(int, lines[2].split())) if n else []
    if len(throughput) != n or len(scaling_cost) != n:
        raise ValueError(f"expected {n} throughput and scalingCost values")
    return throughput, scaling_cost, budget


def part1(lines: list[str]) -> list[str]:
    """'n budget' / n throughput / n scalingCost -> [max min throughput]."""
    throughput, scaling_cost, budget = _read(lines)
    return [str(max_min_throughput(throughput, scaling_cost, budget))]


def part2(lines: list[str]) -> list[str]:
    """same input -> [achieved min throughput, then a line of per-service upgrade counts]."""
    throughput, scaling_cost, budget = _read(lines)
    target, upgrades = max_min_throughput_with_plan(throughput, scaling_cost, budget)
    return [str(target), " ".join(map(str, upgrades))]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
