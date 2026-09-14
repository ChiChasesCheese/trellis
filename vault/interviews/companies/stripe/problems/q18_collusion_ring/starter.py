"""q18 Six Degrees of Collusion — YOUR implementation. Run: python drill.py test q18"""
from __future__ import annotations

import sys

DEFAULT_WEIGHTS = {"name": 0.2, "email": 0.5, "company": 0.3}


def direct_links(records: list[str], target: str) -> list[str]:
    """Part 1: sorted customers (≠ target) sharing an identifier (same position) with target."""
    # TODO
    return []


def groups(records: list[str]) -> list[set[str]]:
    """Part 2: connected components, in order of first-appearing customer."""
    # TODO
    return []


def ring_size(records: list[str], target: str) -> int:
    # TODO
    return 0


def largest_ring(records: list[str]) -> int:
    # TODO
    return 0


def should_block(records: list[str], target: str, k: int) -> bool:
    # TODO
    return False


def ring_risks(records: list[str]) -> list[float]:
    """Part 3: mean risk per ring (zero-risk members removed first), ring order as groups()."""
    # TODO
    return []


def weighted_links(records: list[str], target: str, weights: dict[str, float] = DEFAULT_WEIGHTS,
                   threshold: float = 0.5) -> list[str]:
    """Part 4: records 'user_id,name,email,company'; sorted ids with confidence >= threshold."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out: list[str] = []
    # TODO: dispatch on part (see problem.md for the second-line arguments and output format)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
