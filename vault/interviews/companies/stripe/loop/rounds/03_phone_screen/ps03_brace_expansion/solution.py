"""ps03 Brace Expansion — reference solution.

Three levels of the same idea (glob-style `{a,b,c}` expansion, as in shell filenames or webhook
endpoint templates):
  Part 1 - one un-nested group, well-formed input assumed.
  Part 2 - same scope (at most one group, no nesting) but malformed input must be handled:
           unmatched braces, more than one group, or a group with < 2 comma-separated tokens ->
           the pattern is echoed back unchanged.
  Part 3 - groups may nest and a pattern may contain several groups (cartesian product); the
           same malformed -> echo-unchanged contract now covers the richer grammar.

Order is always preserved (first token first) and duplicates are never deduped or sorted — that
is the deliberate difference from the sorted/deduped LC 1087 style (see `qA03_lc1087_brace_expansion`
in `problems/`): this is a phone-screen "glob expansion" question, not the LeetCode one.

Layout: two scanning helpers (`_find_matching`, `_split_top_commas`) -> `_segments` turns a
pattern into "literal run | group options" pieces -> `_expand` multiplies them (cartesian
product) -> `_is_well_formed` mirrors the same walk but only answers yes/no. Each part is then
one line: validate (or not) + expand.
"""

from __future__ import annotations

import sys

# ------------------------------------------------------------------ scanning helpers


def _find_matching(s: str, i: int) -> int:
    """s[i] == '{'. Index of the matching '}' (brace-depth aware); ValueError if unterminated."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return j
    raise ValueError(f"unterminated group at {i} in {s!r}")


def _split_top_commas(s: str) -> list[str]:
    """Split s on ',' at brace-depth 0 (nested groups keep their own commas)."""
    parts: list[str] = []
    depth, start = 0, 0
    for i, c in enumerate(s):
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(s[start:i])
            start = i + 1
    parts.append(s[start:])
    return parts


# ------------------------------------------------------------------ expansion (well-formed input)


def _segments(s: str) -> list[list[str]]:
    """Cut a well-formed pattern into segments, left to right: a literal run becomes the
    single-option segment [literal]; a `{...}` group becomes its alternatives, each expanded
    recursively and flattened in written order (duplicates kept)."""
    segments: list[list[str]] = []
    i, start = 0, 0
    while i < len(s):
        if s[i] != "{":
            i += 1
            continue
        if start < i:
            segments.append([s[start:i]])
        j = _find_matching(s, i)
        segments.append([out for alt in _split_top_commas(s[i + 1 : j]) for out in _expand(alt)])
        i = start = j + 1
    if start < len(s):
        segments.append([s[start:]])
    return segments


def _expand(s: str) -> list[str]:
    """Cartesian product of the segments; the leftmost segment is the outer loop (bash order).
    A pattern with no group has one literal segment -> [s]; '' -> ['']."""
    results = [""]
    for options in _segments(s):
        results = [r + opt for r in results for opt in options]
    return results


# ------------------------------------------------------------------ validation (Parts 2 & 3)


def _is_well_formed(s: str) -> bool:
    """Braces balanced and properly nested; every group at any depth has >= 2 top-level
    alternatives, each of which is itself well-formed. Same walk as `_segments`, answering yes/no."""
    i = 0
    while i < len(s):
        if s[i] == "}":
            return False  # closing brace with nothing open
        if s[i] != "{":
            i += 1
            continue
        try:
            j = _find_matching(s, i)
        except ValueError:
            return False
        alternatives = _split_top_commas(s[i + 1 : j])
        if len(alternatives) < 2 or not all(_is_well_formed(alt) for alt in alternatives):
            return False
        i = j + 1
    return True


def _has_at_most_one_group(s: str) -> bool:
    """Part 2's scope: a second top-level group and a nested group are both 'a second `{`'."""
    return s.count("{") <= 1


# ------------------------------------------------------------------ public API


def expand_braces(pattern: str) -> list[str]:
    """Part 1: expand a pattern that has at most one, un-nested `{a,b,c}` group. Order preserved,
    prefix/suffix kept, empty tokens allowed (`read.txt{,.bak}`). Input assumed well-formed."""
    return _expand(pattern)


def expand_braces_safe(pattern: str) -> list[str]:
    """Part 2: like expand_braces, but a malformed pattern (unmatched brace, a second/nested
    group, or a group with < 2 tokens) is returned unchanged as the sole result."""
    if not (_has_at_most_one_group(pattern) and _is_well_formed(pattern)):
        return [pattern]
    return _expand(pattern)


def expand_braces_nested(pattern: str) -> list[str]:
    """Part 3: nested groups (`{a,{b,c}}d`) and multiple groups (`{a,b}{1,2}`, cartesian product,
    leftmost group outermost) are now valid input; malformed patterns (checked recursively at
    every depth) are still echoed back unchanged."""
    if not _is_well_formed(pattern):
        return [pattern]
    return _expand(pattern)


def part1(lines: list[str]) -> list[str]:
    return [",".join(expand_braces(p)) for p in lines]


def part2(lines: list[str]) -> list[str]:
    return [",".join(expand_braces_safe(p)) for p in lines]


def part3(lines: list[str]) -> list[str]:
    return [",".join(expand_braces_nested(p)) for p in lines]


PARTS = {1: part1, 2: part2, 3: part3}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out: list[str] = []
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        out = PARTS[part](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
