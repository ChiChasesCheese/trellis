"""ps05 Numeronym validation — YOUR implementation."""

from __future__ import annotations

import sys


def is_valid(numeronym: str) -> bool:
    """True iff numeronym matches ^[a-z][1-9][0-9]*[a-z]$ (see problem.md Part 1)."""
    # TODO
    return False


def part1(lines: list[str]) -> list[str]:
    """lines: raw candidate numeronym strings, one per line (blank lines ignored).
    Return ['VALID'/'INVALID', ...] per candidate, in input order."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """lines[0]: numeronym. lines[1:]: dictionary words, one per line (duplicates count once).
    Return matching dictionary words sorted lexicographically, or ['NONE']."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """lines: dictionary words, one per line. Return ['word -> numeronym', ...] sorted by word,
    with collisions resolved per problem.md Part 3."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    if not raw:
        return
    header, body = raw[0].strip(), raw[1:]
    parts = {"PART 1": part1, "PART 2": part2, "PART 3": part3}
    if header not in parts:
        raise ValueError(f"unknown header: {header!r}")
    out = parts[header](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
