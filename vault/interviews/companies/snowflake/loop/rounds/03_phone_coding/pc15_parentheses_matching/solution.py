"""pc15 Parentheses Matching -- reference solution.

Part1 is LC 20 (Valid Parentheses): three bracket types, `()[]{}` -- a classic stack match.

Part2 and Part3 follow their own original LeetCode problems (LC 921 / LC 32), which are both
defined over a SINGLE bracket type, `(` and `)` only -- Part1's three-type alphabet does not carry
over. Both raise ValueError on any other character.

Part2 (LC 921, Minimum Add to Make Parentheses Valid) returns the minimum number of insertions
AND one concrete resulting valid string, built greedily in a single left-to-right pass: an
unmatched `)` gets a `(` inserted immediately before it; any `(` left unmatched at the end gets a
`)` appended after the whole string.

Part3 (LC 32, Longest Valid Parentheses) returns the length and START INDEX of one longest valid
substring, using the classic stack-of-indices trick (a `-1` sentinel at the bottom marks "the
index just before the current valid run started"). On a tie between multiple maximal-length valid
substrings, the LEFTMOST one is returned (the scan only updates the best on a STRICT `>`).
"""

from __future__ import annotations

import sys

_CLOSE_TO_OPEN = {")": "(", "]": "[", "}": "{"}


def _validate_general(s: str) -> None:
    for ch in s:
        if ch not in "()[]{}":
            raise ValueError(f"unexpected character {ch!r}; only ()[]{{}} are allowed")


def _validate_parens_only(s: str) -> None:
    for ch in s:
        if ch not in "()":
            raise ValueError(f"unexpected character {ch!r}; only '(' and ')' are allowed")


# --------------------------------------------------------------------------- Part 1
def is_valid(s: str) -> bool:
    _validate_general(s)
    stack: list[str] = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        else:
            if not stack or stack.pop() != _CLOSE_TO_OPEN[ch]:
                return False
    return not stack


# --------------------------------------------------------------------------- Part 2
def min_add_to_make_valid(s: str) -> tuple[int, str]:
    _validate_parens_only(s)
    out: list[str] = []
    open_count = 0
    additions = 0
    for ch in s:
        if ch == "(":
            open_count += 1
            out.append(ch)
        elif open_count > 0:
            open_count -= 1
            out.append(ch)
        else:
            additions += 1
            out.append("(")
            out.append(ch)
    additions += open_count
    if open_count:
        out.append(")" * open_count)
    return additions, "".join(out)


# --------------------------------------------------------------------------- Part 3
def longest_valid_substring(s: str) -> tuple[int, int]:
    """(length, start index) of one longest valid substring; leftmost on a tie. (0, 0) if none."""
    _validate_parens_only(s)
    stack = [-1]
    best_len, best_start = 0, 0
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                length = i - stack[-1]
                if length > best_len:
                    best_len = length
                    best_start = stack[-1] + 1
    return best_len, best_start


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """One line: the string -> 'true' or 'false'."""
    return ["true" if is_valid(lines[0]) else "false"]


def part2(lines: list[str]) -> list[str]:
    """One line: the string -> line1 min insertions, line2 one resulting valid string."""
    n, out = min_add_to_make_valid(lines[0])
    return [str(n), out]


def part3(lines: list[str]) -> list[str]:
    """One line: the string -> 'length start_index'."""
    length, start = longest_valid_substring(lines[0])
    return [f"{length} {start}"]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
