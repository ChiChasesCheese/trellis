"""pc13 Service Startup / Dependency Ordering -- YOUR implementation. Run tests with IMPL=starter.

See problem.md: deps are (service, dependency) pairs meaning service requires dependency to have
already started. Ties among simultaneously-ready services break on smallest name.
"""

from __future__ import annotations

import sys


class CycleError(ValueError):
    """Raised when `deps` contains a cycle. `.cycle` lists the services around one such cycle."""

    def __init__(self, cycle: list[str]) -> None:
        self.cycle = cycle
        super().__init__(f"dependency cycle detected: {cycle!r}")


def startup_order(services: list[str], deps: list[tuple[str, str]]) -> list[str]:
    """Part1: Kahn topological order, smallest-name tie-break. Raise CycleError on a cycle."""
    # TODO
    return []


def startup_waves(services: list[str], deps: list[tuple[str, str]]) -> list[list[str]]:
    """Part2: services grouped into parallel startup waves, each wave sorted ascending."""
    # TODO
    return []


def startup_times(
    services: list[str], deps: list[tuple[str, str]], duration: dict[str, int]
) -> tuple[dict[str, int], int]:
    """Part3: (per-service earliest start time, time at which every service is up)."""
    # TODO
    return {}, 0


def part1(lines: list[str]) -> list[str]:
    """'S n' / n service names / 'D m' / m 'service dependency' lines -> the startup order, or
    'CYCLE <c1> <c2> ...' if `deps` contains a cycle."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Same input -> one line per wave: space-separated service names (ascending); or CYCLE line."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Same input plus 'T n' / n 'service duration' lines -> 'earliest_all_up' then one 'service
    start' line per service (ascending by name); or CYCLE line."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
