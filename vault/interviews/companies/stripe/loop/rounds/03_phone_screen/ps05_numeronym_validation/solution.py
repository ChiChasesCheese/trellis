"""ps05 Numeronym validation — reference solution.

Shape: validate (Part 1) -> look up against a dictionary (Part 2) -> generate for a dictionary and
resolve collisions (Part 3). Every part is "parse lines -> pure core -> format lines"; Parts 2/3
reuse Part 1's `is_valid` / the shared dictionary parser instead of re-deriving the rules.

Part 3 collision rule: words sharing (first letter, last letter, length) share a base numeronym.
We grow the kept literal prefix (2, 3, ...) for the whole group until every form is distinct, capped
at len(word) - 2 so the digit segment never drops below 1 (Part 1 requires digit >= 1). If the cap
still leaves a collision, the words differ only in the character right before the last one -- no
valid numeronym can tell them apart -- so every member falls back to its literal spelling.
"""

from __future__ import annotations

import re
import sys

# ------------------------------------------------------------------ rules (constants, one place)
# first char a-z, then digits with no leading zero (value >= 1), then last char a-z.
NUMERONYM_RE = re.compile(r"^[a-z][1-9][0-9]*[a-z]$")
# a dictionary word: lowercase ASCII letters only; anything else is a malformed line and is skipped.
WORD_RE = re.compile(r"^[a-z]+$")
MIN_WORD_LEN = 3  # shortest word that has >= 1 omitted letter (first + 1 middle + last)
NONE_LINE = "NONE"


# ------------------------------------------------------------------ parsing helpers
def _clean_lines(lines: list[str]) -> list[str]:
    """Strip whitespace and drop blank lines (blank lines are ignored everywhere)."""
    return [ln.strip() for ln in lines if ln.strip()]


def _parse_dictionary(lines: list[str]) -> list[str]:
    """Well-formed dictionary words, in first-seen order, duplicates collapsed."""
    return list(dict.fromkeys(w for w in _clean_lines(lines) if WORD_RE.fullmatch(w)))


# ------------------------------------------------------------------ Part 1
def is_valid(numeronym: str) -> bool:
    """True iff `numeronym` has the form letter + digits (no leading zero) + letter."""
    return bool(NUMERONYM_RE.fullmatch(numeronym))


def part1(lines: list[str]) -> list[str]:
    """One 'VALID'/'INVALID' per non-blank candidate line, in input order."""
    return ["VALID" if is_valid(ln) else "INVALID" for ln in _clean_lines(lines)]


# ------------------------------------------------------------------ Part 2
def _expands_to(numeronym: str, word: str) -> bool:
    """True iff `word` could be abbreviated as (valid) `numeronym`: same ends, length = digits + 2."""
    omitted = int(numeronym[1:-1])
    return len(word) == omitted + 2 and word[0] == numeronym[0] and word[-1] == numeronym[-1]


def part2(lines: list[str]) -> list[str]:
    """lines[0] = numeronym, lines[1:] = dictionary. Matching words sorted, or ['NONE']."""
    cleaned = _clean_lines(lines)
    if not cleaned or not is_valid(cleaned[0]):  # nothing an invalid numeronym could stand for
        return [NONE_LINE]
    numeronym, words = cleaned[0], _parse_dictionary(cleaned[1:])
    matches = sorted(w for w in words if _expands_to(numeronym, w))
    return matches or [NONE_LINE]


# ------------------------------------------------------------------ Part 3
def numeronym_for(word: str, prefix_len: int = 1) -> str:
    """Keep `prefix_len` leading letters + count of omitted letters + last letter (prefix 1 = base form)."""
    omitted = len(word) - prefix_len - 1
    return f"{word[:prefix_len]}{omitted}{word[-1]}"


def _resolve_group(group: list[str]) -> dict[str, str]:
    """Disambiguate words that share a base form by growing the literal prefix for the whole group."""
    max_prefix = len(group[0]) - 2  # any longer and the digit segment would hit 0 (invalid per Part 1)
    for prefix_len in range(2, max_prefix + 1):
        forms = [numeronym_for(w, prefix_len) for w in group]
        if len(set(forms)) == len(group):
            return dict(zip(group, forms))
    return {w: w for w in group}  # irreducible: differ only in the char before the last one


def part3(lines: list[str]) -> list[str]:
    """'word -> numeronym' for every distinct dictionary word, sorted by word."""
    result: dict[str, str] = {}
    groups: dict[str, list[str]] = {}  # base numeronym -> words that would produce it
    for word in _parse_dictionary(lines):
        if len(word) < MIN_WORD_LEN:
            result[word] = word  # nothing to omit: the word is its own numeronym
        else:
            groups.setdefault(numeronym_for(word), []).append(word)
    for base, group in groups.items():
        result.update({group[0]: base} if len(group) == 1 else _resolve_group(group))
    return [f"{word} -> {result[word]}" for word in sorted(result)]


# ------------------------------------------------------------------ I/O
PARTS = {"PART 1": part1, "PART 2": part2, "PART 3": part3}


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
