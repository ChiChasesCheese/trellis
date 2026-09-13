"""ps03 Brace Expansion — YOUR implementation. Run: pytest loop/rounds/03_phone_screen/ps03_brace_expansion"""

from __future__ import annotations

import sys


def expand_braces(pattern: str) -> list[str]:
    """Part 1: pattern has at most one, un-nested {tok1,tok2,...} group; input is well-formed.
    Return [prefix+token+suffix, ...], tokens in written order (kept, not sorted or deduped)."""
    # TODO
    return []


def expand_braces_safe(pattern: str) -> list[str]:
    """Part 2: like expand_braces, but a malformed pattern (unmatched brace, a second group, a
    nested group, or a group with < 2 tokens) is returned as [pattern] unchanged."""
    # TODO
    return []


def expand_braces_nested(pattern: str) -> list[str]:
    """Part 3: groups may nest and a pattern may have several groups (cartesian product, left
    group outermost). Malformed detection is recursive; malformed -> [pattern] unchanged."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    return [",".join(expand_braces(p)) for p in lines]


def part2(lines: list[str]) -> list[str]:
    return [",".join(expand_braces_safe(p)) for p in lines]


def part3(lines: list[str]) -> list[str]:
    return [",".join(expand_braces_nested(p)) for p in lines]


PARTS = {1: part1, 2: part2, 3: part3}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out: list[str] = []
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        out = PARTS[part](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
