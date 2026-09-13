"""ps07 Redact card numbers from logs — reference solution.

One engine, four parts. `_scan_candidates` walks a log line once (no backtracking) and yields
`Span(start, end, digit_count)` for every maximal digit run -- when `allow_separators` is on, a
single ' ' or '-' sitting between two digits is absorbed into the run, but never a leading,
trailing or doubled one. `_redact_line` then keeps the spans that qualify (length window, and for
Parts 3/4 also Luhn + brand) and masks them in place, digits only, last 4 digits kept. The parts
differ solely in the two policy flags they pass in: Part 1 ⊂ Part 2 ⊂ Part 3 = Part 4 + stats.
"""

from __future__ import annotations

import sys
from typing import NamedTuple

# ------------------------------------------------------------------ rules (constants, one place)
# (network, length, prefix_len, prefix_min, prefix_max) -- a candidate matches a network iff its
# digit length equals `length` and its first `prefix_len` digits, read as an int, fall in
# [prefix_min, prefix_max]. Multiple rows per network cover disjoint prefix ranges/lengths.
NETWORK_RULES: tuple[tuple[str, int, int, int, int], ...] = (
    ("VISA", 13, 1, 4, 4),
    ("VISA", 16, 1, 4, 4),
    ("VISA", 19, 1, 4, 4),
    ("MASTERCARD", 16, 2, 51, 55),
    ("MASTERCARD", 16, 4, 2221, 2720),
    ("AMEX", 15, 2, 34, 34),
    ("AMEX", 15, 2, 37, 37),
    ("DISCOVER", 16, 4, 6011, 6011),
    ("DISCOVER", 16, 2, 65, 65),
)

MIN_PAN_DIGITS, MAX_PAN_DIGITS = 13, 19  # real-world PAN length window (inclusive)
KEEP_LAST = 4  # digits left visible at the end of a masked span
SEPARATORS = " -"  # Part 2+: may join two digit groups, one at a time


class Span(NamedTuple):
    start: int  # index of the first digit
    end: int  # index one past the last digit
    digit_count: int  # digits only, separators excluded


# ------------------------------------------------------------------ PAN validation (reused from q05)


def luhn_ok(digits: str) -> bool:
    """From the right: double every second digit (starting with the 2nd from the right),
    subtract 9 if > 9, sum all; valid iff sum % 10 == 0."""
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def brand_of(digits: str) -> str | None:
    """Network by length + prefix only (no checksum). None if no rule matches."""
    n = len(digits)
    for name, length, prefix_len, prefix_min, prefix_max in NETWORK_RULES:
        if n == length and prefix_min <= int(digits[:prefix_len]) <= prefix_max:
            return name
    return None


def is_card_number(digits: str) -> bool:
    """True iff digits is a real PAN: right (length, prefix) for some network AND Luhn passes."""
    return brand_of(digits) is not None and luhn_ok(digits)


# ------------------------------------------------------------------ scanning + masking
def _scan_candidates(line: str, allow_separators: bool) -> list[Span]:
    """Single pass: every maximal run of digits, optionally chained through single ' '/'-'
    separators that sit between two digits. A span always starts and ends on a digit. O(len(line)):
    `i` only ever moves forward."""
    spans: list[Span] = []
    n, i = len(line), 0
    while i < n:
        if not line[i].isdigit():
            i += 1
            continue
        start, count = i, 0
        while i < n:
            if line[i].isdigit():
                i, count = i + 1, count + 1
            elif allow_separators and line[i] in SEPARATORS and i + 1 < n and line[i + 1].isdigit():
                i += 1  # absorb one separator, only because a digit follows it
            else:
                break
        spans.append(Span(start, i, count))  # the loop above always stops right after a digit
    return spans


def _mask_span(text: str, count: int) -> str:
    """Mask `text` (a candidate substring, digits + separators) in place: every digit except the
    last KEEP_LAST is replaced with '*'; non-digit separators are copied through unchanged."""
    mask_upto = count - KEEP_LAST
    out = []
    seen = 0
    for ch in text:
        if ch.isdigit():
            out.append("*" if seen < mask_upto else ch)
            seen += 1
        else:
            out.append(ch)
    return "".join(out)


def _qualifies(line: str, span: Span, check_luhn_brand: bool) -> bool:
    """Length window always; Luhn + brand only when the part asks for it."""
    if not MIN_PAN_DIGITS <= span.digit_count <= MAX_PAN_DIGITS:
        return False
    if not check_luhn_brand:
        return True
    digits = "".join(ch for ch in line[span.start : span.end] if ch.isdigit())
    return is_card_number(digits)


def _redact_line(line: str, allow_separators: bool, check_luhn_brand: bool) -> tuple[str, int]:
    """Mask every qualifying span of one line in place. Returns (new_line, spans_redacted)."""
    pieces: list[str] = []  # list-append + one join: no quadratic str += rebuilding
    cursor = redacted = 0
    for span in _scan_candidates(line, allow_separators):
        if not _qualifies(line, span, check_luhn_brand):
            continue
        pieces.append(line[cursor : span.start])
        pieces.append(_mask_span(line[span.start : span.end], span.digit_count))
        cursor, redacted = span.end, redacted + 1
    pieces.append(line[cursor:])
    return "".join(pieces), redacted


# ------------------------------------------------------------------ parts (policy flags only)
def part1(lines: list[str]) -> list[str]:
    """Bare digit runs only, no Luhn/brand filter. See problem.md Part 1."""
    return [_redact_line(ln, allow_separators=False, check_luhn_brand=False)[0] for ln in lines]


def part2(lines: list[str]) -> list[str]:
    """Bare + single space/'-'-separated digit chains, still no Luhn/brand filter."""
    return [_redact_line(ln, allow_separators=True, check_luhn_brand=False)[0] for ln in lines]


def part3(lines: list[str]) -> list[str]:
    """Same scanner as Part 2, but only redacts Luhn+brand-valid candidates."""
    return [_redact_line(ln, allow_separators=True, check_luhn_brand=True)[0] for ln in lines]


def part4(lines: list[str]) -> list[str]:
    """Same detection as Part 3 (already single-pass per line), plus a trailing 'REDACTED n'
    line counting spans actually masked across the whole input."""
    out: list[str] = []
    total = 0
    for ln in lines:
        new_ln, n = _redact_line(ln, allow_separators=True, check_luhn_brand=True)
        out.append(new_ln)
        total += n
    return out + [f"REDACTED {total}"]


PARTS = {"PART 1": part1, "PART 2": part2, "PART 3": part3, "PART 4": part4}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    if not raw:
        return
    header, body = raw[0].strip(), raw[1:]
    if header not in PARTS:
        raise ValueError(f"unknown header: {header!r}")
    out = PARTS[header](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
