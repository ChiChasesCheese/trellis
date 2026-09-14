"""pc11 Character Frequencies -- reference solution.

Part1: count every character across a FLAT list of strings (every character counts, including
spaces and punctuation -- this is a warm-up filler question, not a "letters only" puzzle). Output
sorted by count descending, then character ascending, so ties are deterministic.

Part2 (reconstructed): the input can be an arbitrarily deep nested list of strings, e.g.
`["ab", ["cd", ["ef"]], "gh"]`. Flatten it ITERATIVELY (an explicit stack of iterators, not
recursion) so a pathologically deep nesting (tens of thousands of levels, which a recursive
flattener would blow Python's call stack on) still works, then count exactly as in Part1.

Part3 (reconstructed): top-k characters by the same (count desc, char asc) order, but WITH TIES
INCLUDED -- if several characters share the count that sits at the k-th place, all of them are
returned, so the result can have more than k entries.
"""

from __future__ import annotations

import sys


def _validate_flat(strings: list[str]) -> None:
    for s in strings:
        if not isinstance(s, str):
            raise ValueError(f"expected a flat list of str, got {type(s).__name__}: {s!r}")


def _count(chars) -> dict[str, int]:
    counts: dict[str, int] = {}
    for ch in chars:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


def _sorted_counts(counts: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))


def _iter_flat_chars(strings: list[str]):
    for s in strings:
        yield from s


def _iter_nested_chars(data):
    """Iterative (stack-based) flatten + char yield -- no Python recursion, arbitrary depth."""
    if not isinstance(data, list):
        raise ValueError(f"nested data must be a list, got {type(data).__name__}")
    stack = [iter(data)]
    while stack:
        it = stack[-1]
        try:
            item = next(it)
        except StopIteration:
            stack.pop()
            continue
        if isinstance(item, str):
            yield from item
        elif isinstance(item, list):
            stack.append(iter(item))
        else:
            raise ValueError(f"nested data must contain only str and list, got {type(item).__name__}: {item!r}")


# --------------------------------------------------------------------------- Part 1
def char_frequencies(strings: list[str]) -> list[tuple[str, int]]:
    _validate_flat(strings)
    return _sorted_counts(_count(_iter_flat_chars(strings)))


# --------------------------------------------------------------------------- Part 2
def char_frequencies_nested(data: list) -> list[tuple[str, int]]:
    return _sorted_counts(_count(_iter_nested_chars(data)))


# --------------------------------------------------------------------------- Part 3
def top_k_chars(data: list, k: int) -> list[tuple[str, int]]:
    """Top-k by (count desc, char asc), ties at the cutoff included (so len(result) can exceed k)."""
    if k < 0:
        raise ValueError("k must be >= 0")
    ordered = _sorted_counts(_count(_iter_nested_chars(data)))
    if k == 0 or not ordered:
        return []
    if k >= len(ordered):
        return ordered
    cutoff_count = ordered[k - 1][1]
    end = k
    while end < len(ordered) and ordered[end][1] == cutoff_count:
        end += 1
    return ordered[:end]


# --------------------------------------------------------------------------- line-driven wrappers
def _fmt(pairs: list[tuple[str, int]]) -> list[str]:
    if not pairs:
        return ["-"]
    return [f"{ch} {n}" for ch, n in pairs]


def _read_strings(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    return lines[idx : idx + n], idx + n


def _read_nested(line: str):
    """Iteratively parse one line of nested-list literal syntax, e.g. '["ab", ["cd"], "ef"]'.
    A hand-rolled scanner (explicit stack, not `ast.literal_eval`/`json.loads`) so arbitrarily deep
    nesting doesn't hit the *parser's own* recursion limit -- CPython's literal/JSON parsers are
    themselves recursive and choke around ~100 levels of nested brackets, which would defeat the
    point of an iterative-flatten problem the moment the input has to come from stdin."""
    stack: list[list] = []
    result = None
    i, n = 0, len(line)
    while i < n:
        ch = line[i]
        if ch in " \t\r\n,":
            i += 1
        elif ch == "[":
            stack.append([])
            i += 1
        elif ch == "]":
            if not stack:
                raise ValueError("unbalanced ']' in nested literal")
            finished = stack.pop()
            if stack:
                stack[-1].append(finished)
            else:
                result = finished
            i += 1
        elif ch == '"':
            j = line.find('"', i + 1)
            if j == -1:
                raise ValueError("unterminated string in nested literal")
            if not stack:
                raise ValueError("string literal must be inside a list")
            stack[-1].append(line[i + 1 : j])
            i = j + 1
        else:
            raise ValueError(f"unexpected character {ch!r} in nested literal")
    if stack or result is None:
        raise ValueError("unbalanced brackets in nested literal")
    return result


def part1(lines: list[str]) -> list[str]:
    """'N n' / n string lines -> one 'char count' line per char (desc count, asc char), or '-'."""
    strings, _ = _read_strings(lines, 0)
    return _fmt(char_frequencies(strings))


def part2(lines: list[str]) -> list[str]:
    """One line: a nested-list literal of strings -> same output format as part1."""
    data = _read_nested(lines[0])
    return _fmt(char_frequencies_nested(data))


def part3(lines: list[str]) -> list[str]:
    """'K k' / one line: a nested-list literal -> top-k chars (ties included), same output format."""
    tag, k = lines[0].split()
    if tag != "K":
        raise ValueError(f"expected 'K <k>', got {lines[0]!r}")
    data = _read_nested(lines[1])
    return _fmt(top_k_chars(data, int(k)))


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
