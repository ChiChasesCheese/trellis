"""qA03 LC 1087 Brace Expansion — reference solution.

Part 1 parses the template into segments (each a list of options) with a one-level brace scanner,
then expands iteratively. Part 2 is the backtracking twin. Part 3 handles the nested LC 1096
grammar with a stack of (alternatives, current) frames. Part 4 counts / indexes without expanding.
"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Segment(NamedTuple):
    options: list[str]   # raw tokens (may be empty strings); a literal has exactly one
    is_group: bool       # came from {...}


def parse_segments(s: str) -> list[Segment] | None:
    """Return None when malformed: '{' inside a group, '}' outside one, or an unclosed '{'."""
    segments: list[Segment] = []
    literal: list[str] = []
    group: list[str] | None = None  # tokens of the open group; None when outside braces
    for ch in s:
        if ch == "{":
            if group is not None:
                return None  # nested brace — not allowed in LC 1087
            if literal:
                segments.append(Segment(["".join(literal)], False))
                literal = []
            group = [""]
        elif ch == "}":
            if group is None:
                return None  # '}' before '{'
            segments.append(Segment(group, True))
            group = None
        elif ch == "," and group is not None:
            group.append("")
        elif group is not None:
            group[-1] += ch
        else:
            literal.append(ch)
    if group is not None:
        return None  # unclosed '{'
    if literal:
        segments.append(Segment(["".join(literal)], False))
    return segments


def brace_expansion(s: str, echo_malformed: bool = False) -> list[str]:
    """Part 1: iterative product over segments; result sorted + de-duplicated."""
    segments = parse_segments(s)
    if echo_malformed:
        # screening variant: malformed, no group, or a group with < 2 tokens -> input unchanged
        if segments is None or not any(seg.is_group for seg in segments):
            return [s]
        if any(seg.is_group and len(seg.options) < 2 for seg in segments):
            return [s]
    if segments is None:
        raise ValueError(f"malformed template: {s!r}")
    words = [""]
    for seg in segments:
        words = [w + o for w in words for o in sorted(set(seg.options))]
    return sorted(set(words))


def brace_expansion_recursive(s: str) -> list[str]:
    """Part 2: DFS over segments."""
    segments = parse_segments(s)
    if segments is None:
        raise ValueError(f"malformed template: {s!r}")
    out: set[str] = set()

    def dfs(i: int, prefix: str) -> None:
        if i == len(segments):
            out.add(prefix)
            return
        for o in segments[i].options:
            dfs(i + 1, prefix + o)

    dfs(0, "")
    return sorted(out)


def brace_expansion_nested(s: str) -> list[str]:
    """Part 3 (LC 1096): '{' pushes a frame, ',' closes an alternative, '}' pops and multiplies."""
    stack: list[tuple[list[set[str]], set[str]]] = []
    alternatives: list[set[str]] = []  # completed alternatives of the current frame
    current: set[str] = {""}           # words of the alternative being built
    for ch in s:
        if ch == "{":
            stack.append((alternatives, current))
            alternatives, current = [], {""}
        elif ch == ",":
            alternatives.append(current)
            current = {""}
        elif ch == "}":
            if not stack:
                raise ValueError(f"malformed template: {s!r}")
            alternatives.append(current)
            inner = set().union(*alternatives)  # comma = union (dedupes)
            alternatives, current = stack.pop()
            current = {a + b for a in current for b in inner}  # concatenation = product
        else:
            current = {a + ch for a in current}
    if stack:
        raise ValueError(f"malformed template: {s!r}")
    alternatives.append(current)
    return sorted(set().union(*alternatives))


def _sorted_groups(s: str) -> list[list[str]]:
    segments = parse_segments(s)
    if segments is None:
        raise ValueError(f"malformed template: {s!r}")
    return [sorted(set(seg.options)) for seg in segments]


def count_expansions(s: str) -> int:
    """Part 4: product of distinct-option counts (Python ints, so 10^20 is fine)."""
    n = 1
    for options in _sorted_groups(s):
        n *= len(options)
    return n


def kth_expansion(s: str, k: int) -> str | None:
    """Part 4: mixed-radix decode of k-1, leftmost group most significant."""
    groups = _sorted_groups(s)
    if k < 1 or k > count_expansions(s):
        return None
    idx = k - 1
    chosen: list[str] = []
    for options in reversed(groups):
        idx, d = divmod(idx, len(options))
        chosen.append(options[d])
    return "".join(reversed(chosen))


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    s = lines[1]
    if part == 1:
        out = brace_expansion(s)
    elif part == 2:
        out = brace_expansion_recursive(s)
    elif part == 3:
        out = brace_expansion_nested(s)
    else:
        out = [str(count_expansions(s))]
        if len(lines) > 2:
            w = kth_expansion(s, int(lines[2]))
            out.append("NONE" if w is None else w)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
