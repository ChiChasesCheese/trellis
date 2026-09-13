"""ps08 Min/Max with comparator — YOUR implementation."""

from __future__ import annotations

import sys
from datetime import datetime
from decimal import Decimal
from typing import Callable, NamedTuple

VALID_KEYS = ("amount", "created_at", "country")
VALID_MODES = ("min", "max")


class Record(NamedTuple):
    id: str
    amount: Decimal
    created_at: datetime
    country: str


def _parse_timestamp(raw: str) -> datetime:
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


def parse_records(lines: list[str]) -> list[Record]:
    """lines: raw 'id,amount,created_at,country' lines, blank lines ignored."""
    # TODO
    return []


def min_by_amount(records: list[Record]) -> str | None:
    """id of the record with the smallest amount; first on tie; None if empty."""
    # TODO
    return None


def extreme(records: list[Record], key: str, mode: str) -> str | None:
    """id of the extreme record by `key` in `mode`; first on tie; None if empty.
    Raise ValueError on an unknown key or mode."""
    # TODO
    return None


def extreme_with(records: list[Record], comparator: Callable[[Record, Record], int]) -> str | None:
    """id of the record that is the minimum under `comparator`; first on tie; None if empty.
    Must be a linear scan (O(n) comparator calls), not a full sort."""
    # TODO
    return None


def by_amount_then_created_at(a: Record, b: Record) -> int:
    """Canonical comparator used by PART 3 over stdin: amount ascending, ties by created_at
    ascending."""
    # TODO
    return 0


def extreme_all(records: list[Record], key: str, mode: str) -> list[str]:
    """ids of every record tied for the extreme by `key`/`mode`, sorted ascending by id."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    # TODO
    return ["NONE"]


def part2(lines: list[str]) -> list[str]:
    # TODO
    return ["NONE"]


def part3(lines: list[str]) -> list[str]:
    # TODO
    return ["NONE"]


def part4(lines: list[str]) -> list[str]:
    # TODO
    return ["NONE"]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    if not raw:
        return
    header, body = raw[0].strip(), raw[1:]
    if header == "PART 1":
        out = part1(body)
    elif header == "PART 2":
        out = part2(body)
    elif header == "PART 3":
        out = part3(body)
    elif header == "PART 4":
        out = part4(body)
    else:
        raise ValueError(f"unknown header: {header!r}")
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
