"""q05 Payment Card Validation — YOUR implementation. Run: python drill.py test q05"""
from __future__ import annotations

import sys

# network -> (length, allowed digits per leading position): AMEX 34/37, MC 51-55, VISA 4
NETWORKS = {"AMEX": (15, ("3", "47")), "MASTERCARD": (16, ("5", "12345")), "VISA": (16, ("4",))}


def luhn_ok(digits: str) -> bool:
    # TODO
    return False


def network_of(digits: str) -> str | None:
    """Network by length + prefix, or None."""
    # TODO
    return None


def classify(digits: str) -> str:
    """VISA / MASTERCARD / AMEX / INVALID_CHECKSUM / UNKNOWN_NETWORK."""
    # TODO
    return ""


def masked_counts(masked: str) -> dict[str, int]:
    """network -> number of valid completions of the '*' digits (omit zero counts)."""
    # TODO
    return {}


def recover(observed: str) -> list[tuple[str, str]]:
    """Valid originals one digit-change or one adjacent swap away, sorted, deduped."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """Each line: 16-digit card starting with 4 -> 'VISA' | 'INVALID_CHECKSUM'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Each line: masked card -> ['NETWORK,count', ...] alphabetical (may be empty)."""
    # TODO
    return []


def part4(lines: list[str]) -> list[str]:
    """Each line: 'digits?' -> ['card,NETWORK', ...] ascending numeric (may be empty)."""
    # TODO
    return []


PARTS = {1: part1, 2: part2, 3: part3, 4: part4}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out: list[str] = []
    if lines and lines[0].upper().startswith("PART"):
        out = PARTS[int(lines[0].split()[1])](lines[1:])
    else:  # HackerRank form: Q, then 'Pk card' per line
        if lines and lines[0].isdigit():
            lines = lines[1:]
        for ln in lines:
            tag, card = ln.split()
            out.extend(PARTS[int(tag[1:])]([card]))
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
