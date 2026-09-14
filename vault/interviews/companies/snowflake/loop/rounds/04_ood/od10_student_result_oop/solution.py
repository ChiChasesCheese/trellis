"""od10 Student / Result OOP -- reference solution.

Source (first-hand, 2026-05 AIML intern OA): "Implement Student and Result classes. Result inherits
from Student, stores 3 subject marks, calculates percentage, handles recheck requests. Pass mark is
33.33%." Everything more specific than that is reconstructed and stated in problem.md.

Part1: Student(roll, name) validates its fields; Result(Student) holds exactly three marks 0..100,
percentage() = total / 300 * 100 rounded HALF_UP to 2 decimals (Decimal, never float),
passed() = percentage >= 33.33, and a one-line report.
Part2: a Registry of results; recheck(subject, new_mark) is allowed once per subject, only ever
raises a mark (a lower or equal recheck leaves it unchanged but still uses up the recheck), and
top(k) ranks by percentage desc then roll asc.
"""

from __future__ import annotations

import sys
from decimal import ROUND_HALF_UP, Decimal

PASS_MARK = Decimal("33.33")
SUBJECTS = 3
MAX_MARK = 100


class Student:
    def __init__(self, roll: int, name: str) -> None:
        if not isinstance(roll, int) or roll <= 0:
            raise ValueError(f"roll must be a positive integer, got {roll!r}")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        self.roll = roll
        self.name = name.strip()

    def describe(self) -> str:
        return f"{self.roll} {self.name}"


class Result(Student):
    def __init__(self, roll: int, name: str, marks: list[int]) -> None:
        super().__init__(roll, name)
        if len(marks) != SUBJECTS:
            raise ValueError(f"need exactly {SUBJECTS} marks, got {len(marks)}")
        for m in marks:
            if not isinstance(m, int) or not 0 <= m <= MAX_MARK:
                raise ValueError(f"mark out of range: {m!r}")
        self._marks = list(marks)
        self._rechecked: set[int] = set()

    @property
    def marks(self) -> list[int]:
        return list(self._marks)  # a copy: callers cannot mutate grades behind our back

    def percentage(self) -> Decimal:
        pct = Decimal(sum(self._marks)) * 100 / (SUBJECTS * MAX_MARK)
        return pct.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def passed(self) -> bool:
        return self.percentage() >= PASS_MARK

    def report(self) -> str:
        return f"{self.describe()} {self.percentage()} {'PASS' if self.passed() else 'FAIL'}"

    # ----------------------------------------------------------------- Part 2
    def recheck(self, subject: int, new_mark: int) -> str:
        """subject is 1-based. Returns UPDATED / UNCHANGED / REJECTED."""
        if not isinstance(subject, int) or not 1 <= subject <= SUBJECTS:
            return "REJECTED"
        if not isinstance(new_mark, int) or not 0 <= new_mark <= MAX_MARK:
            return "REJECTED"
        if subject in self._rechecked:
            return "REJECTED"
        self._rechecked.add(subject)
        if new_mark > self._marks[subject - 1]:
            self._marks[subject - 1] = new_mark
            return "UPDATED"
        return "UNCHANGED"


class Registry:
    def __init__(self) -> None:
        self._results: dict[int, Result] = {}

    def add(self, result: Result) -> None:
        if result.roll in self._results:
            raise ValueError(f"duplicate roll {result.roll}")
        self._results[result.roll] = result

    def get(self, roll: int) -> Result:
        if roll not in self._results:
            raise KeyError(roll)
        return self._results[roll]

    def top(self, k: int) -> list[Result]:
        ranked = sorted(self._results.values(), key=lambda r: (-r.percentage(), r.roll))
        return ranked[: max(k, 0)]


# --------------------------------------------------------------------------- command stream
def run_commands(lines: list[str]) -> list[str]:
    """ADD <roll> <name> <m1> <m2> <m3> | REPORT <roll> | RECHECK <roll> <subject> <mark> | TOP <k>.
    Bad ADD -> 'ERROR'; unknown roll -> 'NOT_FOUND'."""
    reg = Registry()
    out: list[str] = []
    for line in lines:
        parts = line.split()
        cmd = parts[0]
        if cmd == "ADD":
            try:
                reg.add(Result(int(parts[1]), parts[2], [int(x) for x in parts[3:]]))
            except (ValueError, IndexError):
                out.append("ERROR")
        elif cmd == "REPORT":
            try:
                out.append(reg.get(int(parts[1])).report())
            except KeyError:
                out.append("NOT_FOUND")
        elif cmd == "RECHECK":
            try:
                out.append(reg.get(int(parts[1])).recheck(int(parts[2]), int(parts[3])))
            except KeyError:
                out.append("NOT_FOUND")
        elif cmd == "TOP":
            ranked = reg.top(int(parts[1]))
            out.append(" ".join(str(r.roll) for r in ranked) if ranked else "-")
        else:
            raise ValueError(f"unknown command {line!r}")
    return out


def part1(lines: list[str]) -> list[str]:
    """ADD / REPORT only."""
    return run_commands(lines)


def part2(lines: list[str]) -> list[str]:
    """ADD / REPORT / RECHECK / TOP."""
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
