"""od07 Throne Inheritance without an initial king -- YOUR implementation. Run the tests against
this file with IMPL=starter. See problem.md for every rule (founder, unknown parent/duplicate
child, death semantics, iterative order, succession)."""

from __future__ import annotations

import sys


class ThroneInheritance:
    def __init__(self) -> None:
        pass  # TODO

    def birth(self, parent_name: str, child_name: str) -> None:
        raise NotImplementedError  # TODO: first call plants the founder; else ValueError rules

    def death(self, name: str) -> None:
        raise NotImplementedError  # TODO: idempotent, never raises, never removes from the tree

    def get_inheritance_order(self) -> list[str]:
        raise NotImplementedError  # TODO: iterative pre-order DFS, skip dead, no recursion

    def succession_after(self, name: str) -> str:
        raise NotImplementedError  # TODO Part3: next living name after <name> in full order


def run_commands(lines: list[str]) -> list[str]:
    """BIRTH <parent> <child> | DEATH <name> | ORDER | SUCCESSOR <name>."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    return run_commands(lines)


def part2(lines: list[str]) -> list[str]:
    return run_commands(lines)


def part3(lines: list[str]) -> list[str]:
    return run_commands(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
