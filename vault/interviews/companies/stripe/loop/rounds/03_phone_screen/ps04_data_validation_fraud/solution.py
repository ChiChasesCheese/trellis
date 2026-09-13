"""ps04 Transaction Data Validation / Fraud Report — reference solution.

Four progressive rule categories over a CSV of transactions, in a fixed priority order:
MISSING_FIELD > BLOCKED_METHOD > AMOUNT_OUT_OF_RANGE > SUSPICIOUS. Every applicable rule is
evaluated independently (a row can trigger more than one code); Part 4 formats the final report,
picking at most the top 2 codes by priority and column-aligning the txn_id.

Money: `decimal.Decimal` throughout, never float. Not the same problem as
`problems/q15_kyc_verification` (KYC column checks / quoted-CSV / reconstructed circular-
dependency rules) -- this is transaction fraud triage: numeric range + blocklist + user-behavior
matching against a historical profile.
"""

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
    """Group non-blank lines under their section header (RULES/BLOCKLIST/PROFILES/TRANSACTIONS),
    in whatever order the headers actually appear (the documented order is fixed, but this does
    not depend on it)."""
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
    """One line: min_amount,max_amount (inclusive bounds, decimal dollars)."""
    if not body:
        return None
    lo, hi = (p.strip() for p in body[0].split(","))
    return Decimal(lo), Decimal(hi)


def parse_blocklist(body: list[str]) -> set[str]:
    """One line, comma-separated payment methods; comparison is case-insensitive. Empty/absent
    line -> empty blocklist."""
    if not body or not body[0].strip():
        return set()
    return {m.strip().lower() for m in body[0].split(",") if m.strip()}


def parse_profiles(body: list[str]) -> dict[str, Profile]:
    """One line per user: user_id,countries,hour_min,hour_max,amount_min,amount_max.
    countries is a ';'-separated set of country codes (commas are the CSV delimiter already)."""
    profiles: dict[str, Profile] = {}
    for ln in body:
        uid, countries, hmin, hmax, amin, amax = (p.strip() for p in ln.split(","))
        profiles[uid] = Profile(
            countries={c.strip().upper() for c in countries.split(";") if c.strip()},
            hour_min=int(hmin),
            hour_max=int(hmax),
            amount_min=Decimal(amin),
            amount_max=Decimal(amax),
        )
    return profiles


def parse_transactions(body: list[str]) -> list[list[str]]:
    """First line is the CSV header (always present, always skipped). Each remaining line is
    split on ',' (fields never contain embedded commas in this problem -- no quoting needed);
    padded to NUM_COLUMNS with '' for missing trailing columns, truncated if there are extras."""
    rows = body[1:] if body else []
    out: list[list[str]] = []
    for ln in rows:
        fields = [f.strip() for f in ln.split(",")]
        fields = (fields + [""] * NUM_COLUMNS)[:NUM_COLUMNS]
        out.append(fields)
    return out


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
    """fields: the 7 raw cell values (txn_id,user_id,amount,currency,payment_method,country,
    timestamp), already trimmed and padded to 7. checks (1..3) gates which rule categories run:
    1 = MISSING_FIELD only; 2 = + BLOCKED_METHOD, AMOUNT_OUT_OF_RANGE; 3 = + SUSPICIOUS.
    Every active rule is evaluated independently; returns the triggered codes in PRIORITY order
    (insertion order below IS priority order -- do not re-sort)."""
    txn_id, user_id, amount_s, currency, method, country, timestamp = fields
    codes: list[str] = []

    if any(f == "" for f in fields):
        codes.append("MISSING_FIELD")

    amount = _try_decimal(amount_s)

    if checks >= 2:
        if method.lower() in blocklist:
            codes.append("BLOCKED_METHOD")
        if amount is not None and rules is not None:
            lo, hi = rules
            if not (lo <= amount <= hi):
                codes.append("AMOUNT_OUT_OF_RANGE")

    if checks >= 3:
        profile = profiles.get(user_id)
        if profile is not None:
            matches = 0
            if country.upper() in profile.countries:
                matches += 1
            hour = _parse_hour(timestamp)
            if hour is not None and profile.hour_min <= hour <= profile.hour_max:
                matches += 1
            if amount is not None and profile.amount_min <= amount <= profile.amount_max:
                matches += 1
            if matches < 2:  # need >= 2 of 3 attributes to match ("at least 50%")
                codes.append("SUSPICIOUS")

    return codes


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
    """Final report: same rule set as part3, but at most the top 2 codes (priority order) and
    column-aligned output -- txn_id left-justified to the widest id in this batch, two spaces,
    then the codes joined by ',' (or 'OK')."""
    rules, blocklist, profiles, txns = _load(lines)
    rows: list[tuple[str, list[str]]] = []
    for f in txns:
        codes = check_row(f, 3, rules, blocklist, profiles)
        rows.append((f[0], codes[:2]))
    width = max((len(txn_id) for txn_id, _ in rows), default=0)
    return [f"{txn_id:<{width}}  {','.join(codes) if codes else 'OK'}" for txn_id, codes in rows]


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
