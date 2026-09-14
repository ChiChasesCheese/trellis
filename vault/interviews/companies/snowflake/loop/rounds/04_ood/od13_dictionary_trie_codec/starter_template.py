"""od13 Dictionary Trie Codec -- YOUR implementation. Run the tests against this file with
IMPL=starter. See problem.md for the exact encoding grammar, the compactness bound, malformed
input rules, and the streaming starts_with() contract."""

from __future__ import annotations

import sys


def serialize(words: list[str]) -> str:
    raise NotImplementedError  # TODO: iterative pre-order emission, see problem.md grammar


def deserialize(data: str) -> list[str]:
    raise NotImplementedError  # TODO: iterative parse, ValueError on malformed input


def starts_with(data: str, prefix: str) -> bool:
    raise NotImplementedError  # TODO Part3: scan-only, do not rebuild the trie


def part1(lines: list[str]) -> list[str]:
    # TODO: SERIALIZE <n> <word...> -> encoded string; DESERIALIZE <data> -> words or "-"
    return []


def part2(lines: list[str]) -> list[str]:
    return part1(lines)


def part3(lines: list[str]) -> list[str]:
    # TODO: same commands as part1, plus STARTSWITH <data> <prefix>; wrap ValueError as "ERROR"
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
