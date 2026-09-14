"""q15 KYC Business Verification — YOUR implementation. Run: python drill.py test q15"""
from __future__ import annotations

import sys

COLUMNS = ["business_name", "business_profile_name", "full_statement_descriptor",
           "short_statement_descriptor", "url", "product_description"]
BLACKLIST = {"ONLINE STORE", "ECOMMERCE", "RETAIL", "SHOP", "GENERAL MERCHANDISE"}
CODES = ["EMPTY_FIELD", "DESCRIPTOR_LENGTH", "DESCRIPTOR_BLACKLISTED", "SHORT_DESCRIPTOR",
         "NAME_MISMATCH", "INVALID_URL"]


def check_row(fields: list[str], part: int = 5) -> list[str]:
    """fields: the 6 trimmed column values. Return failing reason codes in CODES order."""
    # TODO
    return []


def verify(rows: list[str], part: int = 5, reasons: bool = False) -> list[str]:
    """rows: raw CSV lines (header row optional). Return 'VERIFIED: name' / 'NOT VERIFIED: name' lines."""
    # TODO
    return []


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
