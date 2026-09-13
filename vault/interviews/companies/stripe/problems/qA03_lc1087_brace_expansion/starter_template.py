"""qA03 LC 1087 Brace Expansion — YOUR implementation. Run: python drill.py test qA03"""
from __future__ import annotations

import sys


def brace_expansion(s: str, echo_malformed: bool = False) -> list[str]:
    """Part 1: iterative expansion of non-nested {a,b} groups; sorted distinct words.
    echo_malformed=True: malformed template or a group with < 2 tokens -> [s]."""
    # TODO
    return []


def brace_expansion_recursive(s: str) -> list[str]:
    """Part 2: same result by backtracking over segments."""
    # TODO
    return []


def brace_expansion_nested(s: str) -> list[str]:
    """Part 3: LC 1096 grammar (nested groups, comma = union); sorted distinct words."""
    # TODO
    return []


def count_expansions(s: str) -> int:
    """Part 4: number of choice combinations (product of distinct options per group)."""
    # TODO
    return 0


def kth_expansion(s: str, k: int) -> str | None:
    """Part 4: k-th (1-based) word in choice order; None if out of range."""
    # TODO
    return None


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    # TODO: PART n / template / [k]
    stdout.write("")


if __name__ == "__main__":
    main()
