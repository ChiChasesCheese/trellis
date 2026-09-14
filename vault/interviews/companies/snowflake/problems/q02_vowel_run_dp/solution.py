"""q02 Vowel-Run DP — reference solution.

Three variants of the same "count strings by consecutive-vowel-run length" DP family:

Part 1: exact count (Python big int, no modulus), small n.
Part 2: same DP, mod 1e9+7, must stay fast for word_len up to 2500.
Part 3: a different but related counting problem over *actual* strings: count substrings
that are pure-vowel and contain all 5 distinct vowels.

DP for parts 1/2
-----------------
State after i characters: dp[j] = number of valid length-i strings whose current trailing run
of vowels has length exactly j (0 <= j <= k). j == 0 means "ends in a consonant" (or i == 0,
the empty prefix, which is bucketed with "ends in consonant" since it imposes no run).

Transition (i -> i+1):
  - append a consonant (21 ways) to ANY state -> new state 0. So new dp[0] = 21 * sum(dp).
  - append a vowel (5 ways) to a state ending in a run of length j (j < k) -> new state j+1.
    So new dp[j] = 5 * dp[j-1] for j = 1..k (only reachable because dp[k-1] existed at i, and
    extending it to a run of length k is still allowed — k is the max, not the limit-exclusive).

Answer at length n = sum(dp) after n transitions. Because state k can never be extended by
another vowel (that would make a run of length k+1, which is exactly the thing being capped),
capping the state vector at index k is correct and sufficient.

Sanity checks done by hand (see problem.md): ways(1, 0) == 21 (only consonants), ways(1, k>=1)
== 26 (any letter). Both fall out of the DP's base case dp = [1, 0, ..., 0] (dp[0] = 1, i.e. the
empty string) after one transition.
"""
from __future__ import annotations

import sys

VOWELS = frozenset("aeiou")
MOD = 1_000_000_007


def _count_strings(n: int, k: int, mod: int | None) -> int:
    """Shared DP core for part1 (mod=None) and part2 (mod=MOD).

    O(n * min(k, n)) time, O(min(k, n)) space. sum(dp) each step is a single C-level call, so in
    practice this comfortably finishes n=k=2500 well under a second even in pure Python.
    """
    if n < 0 or k < 0:
        raise ValueError("n and k must be non-negative")
    cap = min(k, n)  # states beyond n are unreachable and pointless to track
    dp = [0] * (cap + 1)
    dp[0] = 1  # the empty string: "ends in consonant" bucket, run length 0
    for _ in range(n):
        total = sum(dp)
        if mod is not None:
            total %= mod
        # shift vowel-run states up by one, from the top down so we don't clobber dp[j-1]
        # before it's read.
        for j in range(cap, 0, -1):
            v = dp[j - 1] * 5
            dp[j] = v % mod if mod is not None else v
        dp[0] = total * 21
        if mod is not None:
            dp[0] %= mod
    total = sum(dp)
    return total % mod if mod is not None else total


def part1(n: int, k: int) -> int:
    """Exact count (no modulus) of length-n strings (26-letter alphabet) with no run of more
    than k consecutive vowels."""
    return _count_strings(n, k, mod=None)


def part2(word_len: int, max_vowels: int) -> int:
    """Same as part1 but mod 1_000_000_007, and must stay fast for word_len up to 2500."""
    return _count_strings(word_len, max_vowels, mod=MOD)


def part3(s: str) -> int:
    """Count substrings of s that are entirely vowels AND contain all 5 distinct vowels.

    Split s into maximal vowel-only runs (any consonant breaks a run). Within a run, scan
    left-to-right tracking the last index each vowel was last seen at. Once all 5 vowels have
    appeared, every further extension of the substring's right end keeps it valid as long as the
    left end doesn't cross the earliest of the five "last seen" positions — so the count of valid
    start positions for the current right end j is `min(last.values()) + 1` (indices local to the
    run, so the run's own start is index 0).
    """
    total = 0
    run_start = 0
    n = len(s)
    i = 0
    while i <= n:
        if i == n or s[i] not in VOWELS:
            # close out the run [run_start, i)
            last: dict[str, int] = {}
            for j in range(run_start, i):
                last[s[j]] = j - run_start
                if len(last) == 5:
                    total += min(last.values()) + 1
            run_start = i + 1
        i += 1
    return total


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """stdin format: first line 'PART n'; second line is the part's payload:
    PART 1 / PART 2 -> 'n k' (two ints, space-separated); PART 3 -> the raw string s
    (may be empty, i.e. the second line may be blank or absent). Output: a single integer
    line (no trailing content, no debug output)."""
    lines = stdin.read().split("\n")
    if not lines or lines[0].strip() == "":
        stdout.write("")
        return
    first = lines[0].strip()
    if not first.upper().startswith("PART"):
        raise ValueError("first line must be 'PART n'")
    part = int(first.split()[1])
    payload = lines[1] if len(lines) > 1 else ""
    if part == 1:
        n, k = (int(x) for x in payload.split())
        out = str(part1(n, k))
    elif part == 2:
        word_len, max_vowels = (int(x) for x in payload.split())
        out = str(part2(word_len, max_vowels))
    elif part == 3:
        out = str(part3(payload.rstrip("\r")))
    else:
        raise ValueError(f"unknown part {part}")
    stdout.write(out + "\n")


if __name__ == "__main__":
    main()
