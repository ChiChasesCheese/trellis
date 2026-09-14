"""q24 Maximum Throughput -- YOUR implementation. Run tests against this file with IMPL=starter.

A pipeline of n services in series; throughput = min across services. Upgrading service i costs
scalingCost[i] flat per upgrade and its capacity becomes throughput[i] * (1 + upgrades). Budget
B. Maximise the bottleneck throughput.
"""

from __future__ import annotations

import sys


def max_min_throughput(throughput: list[int], scaling_cost: list[int], budget: int) -> int:
    """Part1: maximum achievable bottleneck throughput within budget."""
    # TODO
    return 0


def max_min_throughput_with_plan(
    throughput: list[int], scaling_cost: list[int], budget: int
) -> tuple[int, list[int]]:
    """Part2 (reconstructed): (achieved bottleneck, per-service upgrade counts)."""
    # TODO
    return 0, []


def part1(lines: list[str]) -> list[str]:
    """'n budget' / n throughput / n scalingCost -> [max min throughput]."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """same input -> [achieved min throughput, then a line of per-service upgrade counts]."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
