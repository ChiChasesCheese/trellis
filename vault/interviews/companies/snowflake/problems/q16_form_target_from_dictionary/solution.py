"""q16 Number of Ways to Form a Target String Given a Dictionary -- reference solution.

Part 1 is LC 1639 verbatim: `words` is a list of same-length lowercase strings
(that shared length must be >= len(target)). Think of them stacked into a grid. To form
`target`, walk through target's characters left to right; for target[i] pick some
column c (strictly greater than the column used for target[i-1]) and some word
row that has target[i] at column c. Each column may supply at most one character
across the WHOLE formation (once used for target[i], it can't be reused for
target[i+1], regardless of which word row is chosen). Count the number of
distinct (column, word) choices mod 1e9+7 -- choosing a different word at the
same column for the same target position counts as a different way.

Part 2 (reconstructed): forget which word supplies each character -- an
interviewer follow-up asks for the lexicographically smallest sequence of column
indices that CAN form target at all (existence + a canonical witness), ignoring
which word row is used. This is a simple greedy: scan columns left to right and
for each target character take the first column (after the previously chosen
one) where any word has that character.
"""
from __future__ import annotations

import sys

MOD = 1_000_000_007


def _validate(words: list[str], target: str) -> None:
    if not words:
        raise ValueError("words must be non-empty")
    if not isinstance(target, str) or not target:
        raise ValueError("target must be a non-empty str")
    m = len(words[0])
    if len(target) > m:
        raise ValueError(f"target length {len(target)} must be <= word length {m}")
    for w in words:
        if not isinstance(w, str) or len(w) != m or not all("a" <= c <= "z" for c in w):
            raise ValueError(f"word must be lowercase, length {m}: {w!r}")
    if not all("a" <= c <= "z" for c in target):
        raise ValueError(f"target must be lowercase a-z only: {target!r}")


def _column_counts(words: list[str]) -> list[list[int]]:
    m = len(words[0])
    cnt = [[0] * 26 for _ in range(m)]
    for w in words:
        for j, ch in enumerate(w):
            cnt[j][ord(ch) - 97] += 1
    return cnt


# --------------------------------------------------------------------------- Part 1
def num_ways_to_form_target(words: list[str], target: str) -> int:
    """LC1639: number of ways to form target, columns strictly increasing, each
    column used at most once overall, mod 1e9+7."""
    _validate(words, target)
    n = len(target)
    cnt = _column_counts(words)
    m = len(cnt)
    dp = [0] * (n + 1)
    dp[0] = 1
    for j in range(m):
        hi = min(j, n - 1)
        for i in range(hi, -1, -1):
            c = cnt[j][ord(target[i]) - 97]
            if c:
                dp[i + 1] = (dp[i + 1] + dp[i] * c) % MOD
    return dp[n]


# --------------------------------------------------------------------------- Part 2
def smallest_column_assignment(words: list[str], target: str) -> list[int]:
    """The lexicographically smallest strictly-increasing sequence of column
    indices that can form target (ignoring which word supplies each character);
    [] if no such sequence exists."""
    _validate(words, target)
    m = len(words[0])
    col_chars = [{w[j] for w in words} for j in range(m)]
    result: list[int] = []
    col = 0
    for ch in target:
        while col < m and ch not in col_chars[col]:
            col += 1
        if col == m:
            return []
        result.append(col)
        col += 1
    return result


# --------------------------------------------------------------------------- line-driven wrappers
def _read(lines: list[str]) -> tuple[list[str], str]:
    n = int(lines[0])
    words = lines[1 : 1 + n]
    target = lines[1 + n]
    return words, target


def part1(lines: list[str]) -> list[str]:
    """'n' / n words / target -> [count mod 1e9+7]."""
    words, target = _read(lines)
    return [str(num_ways_to_form_target(words, target))]


def part2(lines: list[str]) -> list[str]:
    """same input -> [one line: comma-separated column indices, empty if impossible]."""
    words, target = _read(lines)
    return [",".join(map(str, smallest_column_assignment(words, target)))]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
