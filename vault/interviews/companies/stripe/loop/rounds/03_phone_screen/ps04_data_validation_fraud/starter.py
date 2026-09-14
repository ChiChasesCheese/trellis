"""ps04 Transaction Data Validation / Fraud Report — YOUR implementation.
Run: pytest loop/rounds/03_phone_screen/ps04_data_validation_fraud"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation

SECTION_ORDER = ("RULES", "BLOCKLIST", "PROFILES", "TRANSACTIONS")
PRIORITY = ("MISSING_FIELD", "BLOCKED_METHOD", "AMOUNT_OUT_OF_RANGE", "SUSPICIOUS")
NUM_COLUMNS = 7  # txn_id,user_id,amount,currency,payment_method,country,timestamp


@dataclass
class Profile:
    countries: set[str]
    hour_min: int
    hour_max: int
    amount_min: Decimal
    amount_max: Decimal


def _split_sections(lines: list[str]) -> dict[str, list[str]]:
    """Group non-blank lines under their section header."""
    sections: dict[str, list[str]] = {h: [] for h in SECTION_ORDER}
    current: str | None = None
    for raw in lines:
        ln = raw.strip()
        if not ln:
            continue
        if ln in SECTION_ORDER:
            current = ln
            continue
        if current is not None:
            sections[current].append(ln)
    return sections


def _try_decimal(s: str) -> Decimal | None:
    if not s:
        return None
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def parse_rules(body: list[str]) -> tuple[Decimal, Decimal] | None:
    """One line: min_amount,max_amount (inclusive bounds)."""
    # TODO
    return None


def parse_blocklist(body: list[str]) -> set[str]:
    """One line, comma-separated payment methods (case-insensitive comparison)."""
    # TODO
    return set()


def parse_profiles(body: list[str]) -> dict[str, Profile]:
    """One line per user: user_id,countries(;-joined),hour_min,hour_max,amount_min,amount_max."""
    # TODO
    return {}


def parse_transactions(body: list[str]) -> list[list[str]]:
    """First line is the header (skip it). Split each remaining line on ',', trim, pad/truncate
    to NUM_COLUMNS fields."""
    # TODO
    return []


def _parse_hour(timestamp: str) -> int | None:
    if not timestamp:
        return None
    try:
        return datetime.fromisoformat(timestamp).hour
    except ValueError:
        return None


def check_row(
    fields: list[str],
    checks: int,
    rules: tuple[Decimal, Decimal] | None,
    blocklist: set[str],
    profiles: dict[str, Profile],
) -> list[str]:
    """checks=1: MISSING_FIELD only. checks=2: + BLOCKED_METHOD, AMOUNT_OUT_OF_RANGE.
    checks=3: + SUSPICIOUS. Return triggered codes in PRIORITY order."""
    # TODO
    return []


def _load(lines: list[str]):
    sections = _split_sections(lines)
    rules = parse_rules(sections["RULES"])
    blocklist = parse_blocklist(sections["BLOCKLIST"])
    profiles = parse_profiles(sections["PROFILES"])
    txns = parse_transactions(sections["TRANSACTIONS"])
    return rules, blocklist, profiles, txns


def _report_line(txn_id: str, codes: list[str]) -> str:
    return f"{txn_id}: {','.join(codes) if codes else 'OK'}"


def part1(lines: list[str]) -> list[str]:
    rules, blocklist, profiles, txns = _load(lines)
    return [_report_line(f[0], check_row(f, 1, rules, blocklist, profiles)) for f in txns]


def part2(lines: list[str]) -> list[str]:
    rules, blocklist, profiles, txns = _load(lines)
    return [_report_line(f[0], check_row(f, 2, rules, blocklist, profiles)) for f in txns]


def part3(lines: list[str]) -> list[str]:
    rules, blocklist, profiles, txns = _load(lines)
    return [_report_line(f[0], check_row(f, 3, rules, blocklist, profiles)) for f in txns]


def part4(lines: list[str]) -> list[str]:
    """Top 2 codes by priority, column-aligned: txn_id left-justified to the widest id in this
    run, two spaces, then codes joined by ',' (or 'OK')."""
    # TODO
    return []


PARTS = {1: part1, 2: part2, 3: part3, 4: part4}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw_lines = stdin.read().splitlines()
    lines = [ln for ln in raw_lines if ln.strip()]
    out: list[str] = []
    if lines and lines[0].strip().upper().startswith("PART"):
        part = int(lines[0].split()[1])
        out = PARTS[part](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
