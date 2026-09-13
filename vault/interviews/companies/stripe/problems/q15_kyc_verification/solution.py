"""q15 KYC Business Verification — reference solution.

Rules are cumulative: part n applies rules 1..n. Every rule is evaluated independently so a
row can carry several reason codes; codes are reported in the fixed CODES order.
"""
from __future__ import annotations

import csv
import sys

COLUMNS = ["business_name", "business_profile_name", "full_statement_descriptor",
           "short_statement_descriptor", "url", "product_description"]
BLACKLIST = {"ONLINE STORE", "ECOMMERCE", "RETAIL", "SHOP", "GENERAL MERCHANDISE"}
CODES = ["EMPTY_FIELD", "DESCRIPTOR_LENGTH", "DESCRIPTOR_BLACKLISTED", "SHORT_DESCRIPTOR",
         "NAME_MISMATCH", "INVALID_URL"]
FULL_MIN, FULL_MAX = 5, 31     # inclusive
SHORT_MIN, SHORT_MAX = 2, 10   # inclusive


def _norm(s: str) -> str:
    """Trim, collapse inner whitespace, upper-case (used for blacklist comparison)."""
    return " ".join(s.split()).upper()


def _first_word(s: str) -> str:
    words = s.split()
    return words[0].lower() if words else ""


def valid_url(url: str) -> bool:
    low = url.lower()
    for scheme in ("http://", "https://"):
        if low.startswith(scheme):
            host = url[len(scheme):]
            for stop in "/?#":
                host = host.split(stop, 1)[0]
            return "." in host and not host.startswith(".") and not host.endswith(".") and " " not in host \
                and host.split() == [host]  # no whitespace of any kind
    return False


def check_row(fields: list[str], part: int = 5) -> list[str]:
    name, profile, full, short, url, _product = fields
    codes: list[str] = []
    if any(not f for f in fields):                                         # rule 1
        codes.append("EMPTY_FIELD")
    if part >= 2 and not (FULL_MIN <= len(full) <= FULL_MAX):              # rule 2: 5..31 inclusive
        codes.append("DESCRIPTOR_LENGTH")
    if part >= 3 and _norm(full) in BLACKLIST:                             # rule 3: whole string, case-insensitive
        codes.append("DESCRIPTOR_BLACKLISTED")
    if part >= 4:                                                          # rule 4 (reconstructed)
        if not (SHORT_MIN <= len(short) <= SHORT_MAX) or _first_word(short) != _first_word(full):
            codes.append("SHORT_DESCRIPTOR")
        f = full.lower()
        if not ((name and name.lower() in f) or (profile and profile.lower() in f)):
            codes.append("NAME_MISMATCH")
    if part >= 5 and not valid_url(url):                                   # rule 5 (reconstructed)
        codes.append("INVALID_URL")
    return codes


def parse_rows(rows: list[str]) -> list[list[str]]:
    """csv-parse raw lines: skip blanks and a header row; pad/trim to 6 trimmed fields."""
    out = []
    for rec in csv.reader(ln for ln in rows if ln.strip()):
        fields = [f.strip() for f in rec]
        if not out and fields and fields[0].lower() == COLUMNS[0]:
            continue  # header row (only recognised as the first non-blank row)
        fields = (fields + [""] * len(COLUMNS))[: len(COLUMNS)]
        out.append(fields)
    return out


def verify(rows: list[str], part: int = 5, reasons: bool = False) -> list[str]:
    lines = []
    for fields in parse_rows(rows):
        codes = check_row(fields, part)
        if not codes:
            lines.append(f"VERIFIED: {fields[0]}")
        elif reasons:
            lines.append(f"NOT VERIFIED: {fields[0]} ({', '.join(codes)})")
        else:
            lines.append(f"NOT VERIFIED: {fields[0]}")
    return lines


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    part, reasons = 5, False
    if lines and lines[0].strip().upper().startswith("PART "):
        toks = lines.pop(0).split()
        part, reasons = int(toks[1]), "REASONS" in [t.upper() for t in toks[2:]]
    out = verify(lines, part=part, reasons=reasons)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
