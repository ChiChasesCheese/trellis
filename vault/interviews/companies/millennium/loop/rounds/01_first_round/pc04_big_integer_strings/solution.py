"""pc04 Big-Integer String Arithmetic -- reference solution.

Grade-school arithmetic on decimal digit strings, the way you would do it on paper: no
`int()` conversion anywhere in the core logic (the interview point is showing the manual
carry/borrow bookkeeping, not Python's native bigints).

Part1 is unsigned decimal addition. Part2 adds a sign (+/-) and turns "subtraction" into
"add the negation", comparing magnitudes to decide the result's sign. Part3 generalises the
one operation that is genuinely harder than repeated addition -- multiplication -- to an
arbitrary base 2..36 (digits '0'-'9' then 'a'-'z'), O(n*m) grade-school long multiplication.
"""

from __future__ import annotations

import sys

_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"
_VALUE = {c: i for i, c in enumerate(_DIGITS)}


def _validate_magnitude(s: str, base: int) -> None:
    if not s:
        raise ValueError("operand must not be empty")
    for ch in s:
        if ch not in _VALUE or _VALUE[ch] >= base:
            raise ValueError(f"{ch!r} is not a valid digit in base {base}")


def _strip_leading_zeros(s: str) -> str:
    i = 0
    while i < len(s) - 1 and s[i] == "0":
        i += 1
    return s[i:]


def _strip_sign(s: str) -> tuple[bool, str]:
    """('' is invalid) -> (is_negative, magnitude_without_sign)."""
    if not s:
        raise ValueError("operand must not be empty")
    if s[0] == "-":
        return True, s[1:]
    if s[0] == "+":
        return False, s[1:]
    return False, s


def _cmp_magnitude(a: str, b: str) -> int:
    """-1/0/1, comparing two non-negative decimal-digit strings by value."""
    a, b = _strip_leading_zeros(a), _strip_leading_zeros(b)
    if len(a) != len(b):
        return -1 if len(a) < len(b) else 1
    if a == b:
        return 0
    return -1 if a < b else 1  # same length: lexicographic == numeric for '0'-'9'


def _add_magnitude(a: str, b: str, base: int) -> str:
    """O(max(len(a), len(b))): schoolbook addition with carry, right to left."""
    i, j, carry = len(a) - 1, len(b) - 1, 0
    out: list[str] = []
    while i >= 0 or j >= 0 or carry:
        da = _VALUE[a[i]] if i >= 0 else 0
        db = _VALUE[b[j]] if j >= 0 else 0
        carry, rem = divmod(da + db + carry, base)
        out.append(_DIGITS[rem])
        i -= 1
        j -= 1
    return _strip_leading_zeros("".join(reversed(out)))


def _sub_magnitude(a: str, b: str, base: int) -> str:
    """O(len(a)): schoolbook subtraction with borrow. Requires |a| >= |b| (both already
    stripped of leading zeros by the caller)."""
    i, j, borrow = len(a) - 1, len(b) - 1, 0
    out: list[str] = []
    while i >= 0:
        da = _VALUE[a[i]]
        db = _VALUE[b[j]] if j >= 0 else 0
        total = da - db - borrow
        if total < 0:
            total += base
            borrow = 1
        else:
            borrow = 0
        out.append(_DIGITS[total])
        i -= 1
        j -= 1
    return _strip_leading_zeros("".join(reversed(out)))


# --------------------------------------------------------------------------- Part 1
def add_unsigned(a: str, b: str) -> str:
    """Add two non-negative decimal digit strings. Leading zeros in the operands are
    tolerated ("007"); '' is invalid; non-digit characters raise ValueError."""
    if not a or not b:
        raise ValueError("operand must not be empty")
    _validate_magnitude(a, 10)
    _validate_magnitude(b, 10)
    return _add_magnitude(a, b, 10)


# --------------------------------------------------------------------------- Part 2
def add_signed(a: str, b: str) -> str:
    """Decimal add with an optional leading '-' (or '+') sign. "0" is never signed."""
    neg_a, mag_a = _strip_sign(a)
    neg_b, mag_b = _strip_sign(b)
    _validate_magnitude(mag_a, 10)
    _validate_magnitude(mag_b, 10)
    if neg_a == neg_b:
        result = _add_magnitude(mag_a, mag_b, 10)
        return ("-" + result) if (neg_a and result != "0") else result
    cmp = _cmp_magnitude(mag_a, mag_b)
    if cmp == 0:
        return "0"
    if cmp > 0:
        result = _sub_magnitude(_strip_leading_zeros(mag_a), _strip_leading_zeros(mag_b), 10)
        return ("-" + result) if neg_a else result
    result = _sub_magnitude(_strip_leading_zeros(mag_b), _strip_leading_zeros(mag_a), 10)
    return ("-" + result) if neg_b else result


def _negate(s: str) -> str:
    neg, mag = _strip_sign(s)
    _validate_magnitude(mag, 10)
    mag = _strip_leading_zeros(mag)
    if mag == "0":
        return "0"
    return mag if neg else "-" + mag


def subtract_signed(a: str, b: str) -> str:
    """a - b, by adding the negation of b. Same sign/zero normalisation as add_signed."""
    return add_signed(a, _negate(b))


# --------------------------------------------------------------------------- Part 3
def multiply_signed(a: str, b: str, base: int = 10) -> str:
    """Signed multiplication in an arbitrary base (2..36, digits '0'-'9' then 'a'-'z',
    case-insensitive on input). O(len(a) * len(b)) grade-school long multiplication --
    never converts through int()."""
    if base < 2 or base > 36:
        raise ValueError(f"base must be in [2, 36], got {base}")
    neg_a, mag_a = _strip_sign(a.lower())
    neg_b, mag_b = _strip_sign(b.lower())
    _validate_magnitude(mag_a, base)
    _validate_magnitude(mag_b, base)
    mag_a = _strip_leading_zeros(mag_a)
    mag_b = _strip_leading_zeros(mag_b)
    if mag_a == "0" or mag_b == "0":
        return "0"

    da = [_VALUE[c] for c in reversed(mag_a)]
    db = [_VALUE[c] for c in reversed(mag_b)]
    acc = [0] * (len(da) + len(db))
    for i, x in enumerate(da):
        carry = 0
        for j, y in enumerate(db):
            total = acc[i + j] + x * y + carry
            acc[i + j] = total % base
            carry = total // base
        k = i + len(db)
        while carry:
            total = acc[k] + carry
            acc[k] = total % base
            carry = total // base
            k += 1

    while len(acc) > 1 and acc[-1] == 0:
        acc.pop()
    digits = "".join(_DIGITS[d] for d in reversed(acc))
    return ("-" + digits) if (neg_a != neg_b) else digits


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """each line: '<a> <b>' -> add_unsigned(a, b)."""
    out = []
    for line in lines:
        a, b = line.split()
        out.append(add_unsigned(a, b))
    return out


def part2(lines: list[str]) -> list[str]:
    """each line: 'ADD <a> <b>' or 'SUB <a> <b>'."""
    out = []
    for line in lines:
        op, a, b = line.split()
        if op == "ADD":
            out.append(add_signed(a, b))
        elif op == "SUB":
            out.append(subtract_signed(a, b))
        else:
            raise ValueError(f"unknown op {op!r}")
    return out


def part3(lines: list[str]) -> list[str]:
    """each line: '<a> <b> <base>' -> multiply_signed(a, b, base)."""
    out = []
    for line in lines:
        a, b, base = line.split()
        out.append(multiply_signed(a, b, int(base)))
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
