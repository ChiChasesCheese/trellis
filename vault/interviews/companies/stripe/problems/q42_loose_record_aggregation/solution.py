"""q42 Loose-Schema Record Aggregation — reference solution.

Parsing produces a plain dict per record (last-wins on duplicate keys, malformed tokens
dropped) so Parts 2 and 3 reuse the exact same aggregation helper as Part 1 -- see the
"Interviewer notes" quoted in problem.md's Sources section for why that separation matters.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from typing import Optional

AMOUNT_RE = re.compile(r"^[0-9]+$")
MISSING_GROUP_LABEL = "__none__"
SCHEMA_HEADER = "SCHEMA"


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse_record(line: str) -> dict[str, str]:
    """One record line -> dict of key=value. Malformed tokens (no '=', or empty key) are
    dropped, not errors. Duplicate keys: last occurrence wins (dict assignment order)."""
    fields: dict[str, str] = {}
    for token in line.strip().split():
        if "=" not in token:
            continue
        key, _, value = token.partition("=")
        if not key:
            continue
        fields[key] = value
    return fields


def _parse_records(lines: list[str], n: int) -> list[dict[str, str]]:
    return [parse_record(line) for line in lines[:n]]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def extract_valid_amount_and_currency(record: dict[str, str]) -> Optional[tuple[int, str]]:
    """(amount, currency) if the record is valid for aggregation, else None.

    Valid iff `currency` is present and non-empty (after stripping), and `amount` is a
    non-negative base-10 integer literal (digits only -- no sign, no underscores, no decimal
    point; empty or absent is invalid).
    """
    currency = record.get("currency", "").strip()
    if not currency:
        return None
    raw_amount = record.get("amount", "")
    if not AMOUNT_RE.fullmatch(raw_amount):
        return None
    return int(raw_amount), currency


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


def aggregate_totals(
    records: list[dict[str, str]], group_by_field: Optional[str]
) -> dict:
    """Sum amounts per currency (group_by_field=None) or per (group, currency)."""
    totals: dict = defaultdict(int)
    for record in records:
        valid = extract_valid_amount_and_currency(record)
        if valid is None:
            continue
        amount, currency = valid
        if group_by_field is None:
            key = currency
        else:
            group = record.get(group_by_field, MISSING_GROUP_LABEL)
            key = (group, currency)
        totals[key] += amount
    return dict(totals)


def schema_counts(records: list[dict[str, str]]) -> dict[str, int]:
    """key -> number of records containing that key (including invalid/unknown ones)."""
    counts: dict[str, int] = defaultdict(int)
    for record in records:
        for key in record:
            counts[key] += 1
    return dict(counts)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_totals(totals: dict, grouped: bool) -> list[str]:
    if not grouped:
        return [f"{currency} {totals[currency]}" for currency in sorted(totals)]
    return [f"{group} {currency} {totals[(group, currency)]}" for group, currency in sorted(totals)]


def render_schema(counts: dict[str, int]) -> list[str]:
    lines = [SCHEMA_HEADER]
    lines.extend(f"{key} {counts[key]}" for key in sorted(counts))
    return lines


# ---------------------------------------------------------------------------
# Parts
# ---------------------------------------------------------------------------


def part1(lines: list[str]) -> list[str]:
    """Header 'N', then N record lines -> total amount per currency, sorted by currency."""
    if not lines:
        return []
    n = int(lines[0].split()[0])
    records = _parse_records(lines[1:], n)
    totals = aggregate_totals(records, None)
    return render_totals(totals, grouped=False)


def part2(lines: list[str]) -> list[str]:
    """Header 'N group_by_key', then N record lines -> total per (group, currency)."""
    if not lines:
        return []
    tokens = lines[0].split()
    n = int(tokens[0])
    group_key = tokens[1] if len(tokens) >= 2 else None
    records = _parse_records(lines[1:], n)
    totals = aggregate_totals(records, group_key)
    return render_totals(totals, grouped=True)


def part3(lines: list[str]) -> list[str]:
    """Header 'N' or 'N group_by_key', then N record lines -> totals + SCHEMA block."""
    if not lines:
        return []
    tokens = lines[0].split()
    n = int(tokens[0])
    group_key = tokens[1] if len(tokens) >= 2 else None
    records = _parse_records(lines[1:], n)
    totals = aggregate_totals(records, group_key)
    out = render_totals(totals, grouped=group_key is not None)
    out.extend(render_schema(schema_counts(records)))
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    if not raw or not raw[0].strip():
        return
    part = int(raw[0].split()[1])
    fn = {1: part1, 2: part2, 3: part3}[part]
    out = fn(raw[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
