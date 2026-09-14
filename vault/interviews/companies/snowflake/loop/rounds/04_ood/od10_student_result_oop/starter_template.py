"""od10 Student / Result OOP -- YOUR implementation. Run the tests against this file with
IMPL=starter. See problem.md for every rule (validation, rounding, recheck, ranking)."""

from __future__ import annotations

import sys
from decimal import Decimal

PASS_MARK = Decimal("33.33")


class Student:
    def __init__(self, roll: int, name: str) -> None:
        raise NotImplementedError  # TODO: validate; roll > 0, name non-blank

    def describe(self) -> str:
        raise NotImplementedError  # TODO: "<roll> <name>"


class Result(Student):
    def __init__(self, roll: int, name: str, marks: list[int]) -> None:
        raise NotImplementedError  # TODO: exactly 3 marks in 0..100

    @property
    def marks(self) -> list[int]:
        raise NotImplementedError  # TODO: return a copy

    def percentage(self) -> Decimal:
        raise NotImplementedError  # TODO: Decimal, HALF_UP, 2 places

    def passed(self) -> bool:
        raise NotImplementedError  # TODO

    def report(self) -> str:
        raise NotImplementedError  # TODO: "<roll> <name> <pct> PASS|FAIL"

    def recheck(self, subject: int, new_mark: int) -> str:
        raise NotImplementedError  # TODO Part2: UPDATED / UNCHANGED / REJECTED


class Registry:
    def __init__(self) -> None:
        pass  # TODO

    def add(self, result: Result) -> None:
        raise NotImplementedError  # TODO: ValueError on duplicate roll

    def get(self, roll: int) -> Result:
        raise NotImplementedError  # TODO: KeyError if missing

    def top(self, k: int) -> list[Result]:
        raise NotImplementedError  # TODO: percentage desc, roll asc


def run_commands(lines: list[str]) -> list[str]:
    """ADD <roll> <name> <m1> <m2> <m3> | REPORT <roll> | RECHECK <roll> <subject> <mark> | TOP <k>."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    return run_commands(lines)


def part2(lines: list[str]) -> list[str]:
    return run_commands(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
