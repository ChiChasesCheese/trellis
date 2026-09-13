"""ps08 Min/Max with comparator — reference solution.

Record is a small NamedTuple (id, amount: Decimal, created_at: datetime, country: str), parsed
once by `parse_records`. Parts 1-3 all resolve ties to the first record in input order; Part 4
is the one place that contract changes (return every tied record, sorted by id) -- called out
explicitly in problem.md and in REPORT.md rather than left as a silent inconsistency.
"""

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
    # datetime.fromisoformat accepts 'Z' natively from Python 3.11; normalize defensively so
    # this also runs correctly on 3.10 and earlier.
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


def parse_records(lines: list[str]) -> list[Record]:
    """lines: raw 'id,amount,created_at,country' lines, blank lines ignored."""
    records = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        rid, amount, created_at, country = (p.strip() for p in raw.split(","))
        records.append(Record(rid, Decimal(amount), _parse_timestamp(created_at), country))
    return records


def _key_extractor(key: str) -> Callable[[Record], object]:
    if key == "amount":
        return lambda r: r.amount
    if key == "created_at":
        return lambda r: r.created_at
    if key == "country":
        return lambda r: r.country
    raise ValueError(f"unknown key: {key!r}")


def min_by_amount(records: list[Record]) -> str | None:
    """id of the record with the smallest amount; first on tie; None if empty."""
    best: Record | None = None
    for r in records:
        if best is None or r.amount < best.amount:
            best = r
    return best.id if best is not None else None


def extreme(records: list[Record], key: str, mode: str) -> str | None:
    """id of the extreme record by `key` (amount/created_at/country) in `mode` (min/max);
    first on tie; None if empty. Raises ValueError on an unknown key or mode."""
    if mode not in VALID_MODES:
        raise ValueError(f"unknown mode: {mode!r}")
    extract = _key_extractor(key)
    best: Record | None = None
    best_val = None
    for r in records:
        val = extract(r)
        if best is None:
            best, best_val = r, val
            continue
        if (mode == "min" and val < best_val) or (mode == "max" and val > best_val):
            best, best_val = r, val
    return best.id if best is not None else None


def extreme_with(records: list[Record], comparator: Callable[[Record, Record], int]) -> str | None:
    """id of the record that is the minimum under `comparator` (a, b) -> negative/0/positive;
    linear scan (O(n) comparator calls), first on tie. For 'max' under a comparator, pass a
    comparator with the sign flipped. None if empty."""
    best: Record | None = None
    for r in records:
        if best is None or comparator(r, best) < 0:
            best = r
    return best.id if best is not None else None


def by_amount_then_created_at(a: Record, b: Record) -> int:
    """Canonical demo comparator for PART 3 over stdin: amount ascending, ties broken by
    created_at ascending. Expresses an ordering extreme()'s single (key, mode) cannot."""
    if a.amount != b.amount:
        return -1 if a.amount < b.amount else 1
    if a.created_at != b.created_at:
        return -1 if a.created_at < b.created_at else 1
    return 0


def extreme_all(records: list[Record], key: str, mode: str) -> list[str]:
    """ids of every record tied for the extreme by `key`/`mode`, sorted ascending by id.
    Empty list if `records` is empty (part4() renders that as ['NONE'])."""
    if not records:
        return []
    if mode not in VALID_MODES:
        raise ValueError(f"unknown mode: {mode!r}")
    extract = _key_extractor(key)
    extreme_val = extract(records[0])
    for r in records[1:]:
        val = extract(r)
        if (mode == "min" and val < extreme_val) or (mode == "max" and val > extreme_val):
            extreme_val = val
    return sorted(r.id for r in records if extract(r) == extreme_val)


def part1(lines: list[str]) -> list[str]:
    records = parse_records(lines)
    winner = min_by_amount(records)
    return [winner] if winner is not None else ["NONE"]


def part2(lines: list[str]) -> list[str]:
    key, mode = lines[0].split()
    records = parse_records(lines[1:])
    winner = extreme(records, key, mode)
    return [winner] if winner is not None else ["NONE"]


def part3(lines: list[str]) -> list[str]:
    records = parse_records(lines)
    winner = extreme_with(records, by_amount_then_created_at)
    return [winner] if winner is not None else ["NONE"]


def part4(lines: list[str]) -> list[str]:
    key, mode = lines[0].split()
    records = parse_records(lines[1:])
    tied = extreme_all(records, key, mode)
    return tied if tied else ["NONE"]


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
