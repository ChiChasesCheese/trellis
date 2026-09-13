"""q06 Atlas Company Name Availability — YOUR implementation. Run: python drill.py test q06"""
from __future__ import annotations

import sys

SUFFIXES = {"inc", "inc.", "corp", "corp.", "llc", "l.l.c.", "llc."}
ARTICLES = {"the", "a", "an"}


def normalize(name: str, strip_punctuation: bool = True) -> str:
    """Canonical form ('' means unusable). See problem.md steps 1-8."""
    # TODO
    return ""


def split_input(lines: list[str]) -> tuple[list[str], list[str]]:
    """-> (registered names from the REGISTERED block, request lines)."""
    # TODO
    return [], []


def part1(lines: list[str], persist: bool = False) -> list[str]:
    """Stateless check against the REGISTERED block (persist=True registers accepted names)."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Persistent registry: accepted names are taken by that account from then on."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Part 2 + 'RECLAIM,account_id,name' frees the name if account_id is the registrant."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 3
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
