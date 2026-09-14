"""pc21 Accumulator Interpreter -- YOUR implementation. Run the tests against this file with
IMPL=starter.
"""

from __future__ import annotations

import sys

MOD = 1_000_000_007


def run_calculator(commands: list[str]) -> int:
    """Part1: accumulator starts at 0. ADD/SUB/MULT/DIV n. DIV truncates toward zero; dividing
    by zero raises ValueError. Unknown command -> ValueError."""
    # TODO
    return 0


def run_snowcal(lines: list[str]) -> int:
    """Part2: X starts at 0. ADD n / MUL n / 'FUN name' ... 'END' (declares a function, body is
    NOT run at declaration) / INV name (runs the function's body in place). ValueError for an
    INV of an undefined function, or for a call cycle (direct or indirect self-recursion)."""
    # TODO
    return 0


def run_snowcal_mod(lines: list[str]) -> int:
    """Part3: same language as Part2 plus 'REPEAT count name' (invoke `name` count times,
    count up to ~10**15). All arithmetic mod 1_000_000_007. Must stay fast for huge counts --
    memoise each function as an affine map x -> a*x + b, and use fast modular exponentiation to
    repeat it count times in O(log count)."""
    # TODO
    return 0


def part1(lines: list[str]) -> list[str]:
    """each line is one program (commands separated by ';') -> the final accumulator."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """lines[0] = 'N', then N instruction lines -> a single line with the final X."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
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
