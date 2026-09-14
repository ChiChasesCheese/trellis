"""od15 JSON Parser -- YOUR implementation. Run the tests against this file with IMPL=starter.
See problem.md for the exact grammar (numbers, string escapes), the canonical re-escaping rule,
the iterative depth requirement, duplicate-key policy, and the path query language.

`json` (stdlib) may be used in tests to cross-check, but must never be imported here."""

from __future__ import annotations

import sys


def parse(text: str, on_duplicate_key: str = "last") -> tuple:
    raise NotImplementedError  # TODO: tokenize + iterative structural parse, see problem.md


def serialize(value: tuple) -> str:
    raise NotImplementedError  # TODO: iterative minified output


def minify(text: str) -> str:
    raise NotImplementedError  # TODO: parse(text) then serialize(...)


def query_path(value: tuple, path: str) -> str:
    raise NotImplementedError  # TODO Part3: "a.b[2].c" style path


def part1(lines: list[str]) -> list[str]:
    # TODO: "PARSE <json>" -> minified text or "INVALID"
    return []


def part2(lines: list[str]) -> list[str]:
    return part1(lines)


def part3(lines: list[str]) -> list[str]:
    # TODO: "PARSE_DUP <last|error> <json>" and "PATH <path> <json>"
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    body = [ln for ln in lines[1:] if ln.strip()]
    out = {1: part1, 2: part2, 3: part3}[n](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
