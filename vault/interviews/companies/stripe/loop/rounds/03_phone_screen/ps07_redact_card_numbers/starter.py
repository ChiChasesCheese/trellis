"""ps07 Redact card numbers from logs — YOUR implementation."""

from __future__ import annotations

import sys

# (network, length, prefix_len, prefix_min, prefix_max) -- fill in the table from problem.md's
# Networks and Luhn section (VISA 13/16/19 prefix 4; MASTERCARD 16 prefix 51-55 or 2221-2720;
# AMEX 15 prefix 34/37; DISCOVER 16 prefix 6011/65).
NETWORK_RULES: tuple[tuple[str, int, int, int, int], ...] = ()

MIN_PAN_DIGITS = 13
MAX_PAN_DIGITS = 19
KEEP_LAST = 4


def luhn_ok(digits: str) -> bool:
    """True iff `digits` passes the Luhn checksum (see problem.md)."""
    # TODO
    return False


def brand_of(digits: str) -> str | None:
    """Network name by length + prefix only (no checksum); None if no NETWORK_RULES row matches."""
    # TODO
    return None


def is_card_number(digits: str) -> bool:
    """True iff `digits` is a real PAN: right (length, prefix) for some network AND Luhn passes."""
    # TODO
    return False


def part1(lines: list[str]) -> list[str]:
    """Bare 13-19 digit runs, no Luhn/brand filter. Return the log lines with each qualifying
    run's leading digits replaced by '*', last 4 digits kept. Non-qualifying lines pass through
    unchanged. Every input line produces exactly one output line, in order (blank lines too)."""
    # TODO
    return list(lines)


def part2(lines: list[str]) -> list[str]:
    """Like part1, but a candidate may also be digit groups joined by a single ' ' or '-'."""
    # TODO
    return list(lines)


def part3(lines: list[str]) -> list[str]:
    """Like part2, but only redact candidates that pass is_card_number (Luhn + brand)."""
    # TODO
    return list(lines)


def part4(lines: list[str]) -> list[str]:
    """Like part3, but append a trailing 'REDACTED n' line counting spans actually redacted.
    Must run in O(total input length) -- no re-scans per line, no backtracking regex."""
    # TODO
    return list(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    if not raw:
        return
    header, body = raw[0].strip(), raw[1:]
    parts = {"PART 1": part1, "PART 2": part2, "PART 3": part3, "PART 4": part4}
    if header not in parts:
        raise ValueError(f"unknown header: {header!r}")
    out = parts[header](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
