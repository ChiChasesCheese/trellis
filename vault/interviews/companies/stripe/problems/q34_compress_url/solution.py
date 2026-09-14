"""q34 Compress URL — reference solution.

A numeronym is first letter + count of letters in between + last letter. Part 2 folds the tail of
a major part (from the m-th minor part to the end) into ONE numeronym where the dots between the
folded minor parts count as characters (that is what the source's Java driver produces:
"section/how.to.write.a.java.program.in.one.day", m=3 -> "s5n/h1w.t0o.w29y").
"""
from __future__ import annotations

import sys
from collections import defaultdict


def numeronym(word: str, min_len: int = 0) -> str:
    """'stripe' -> 's4e'. Part 3: strictly shorter than min_len -> unchanged (len == min_len compresses).
    min_len=0 (Parts 1-2) always compresses, exactly like the source's Java ('to' -> 't0o', 'a' -> 'a-1a')."""
    if len(word) < max(min_len, 1):        # never index into an empty string
        return word
    return f"{word[0]}{len(word) - 2}{word[-1]}"


def compress(url: str, m: int | None = None, min_len: int = 0) -> str:
    majors = []
    for major in url.split("/"):
        minors = major.split(".")
        if m is not None and len(minors) > m:  # strictly more than m -> fold; == m is untouched
            head = [numeronym(w, min_len) for w in minors[: m - 1]]
            tail = ".".join(minors[m - 1 :])   # dots inside the tail are counted
            minors_out = head + [numeronym(tail, min_len)]
        else:
            minors_out = [numeronym(w, min_len) for w in minors]
        majors.append(".".join(minors_out))
    return "/".join(majors)


def ambiguous(urls: list[str]) -> list[str]:
    originals: dict[str, set[str]] = defaultdict(set)
    for u in urls:
        originals[compress(u)].add(u)         # a set: exact duplicate URLs count once
    return [f"{c}: {len(s)}" for c, s in sorted(originals.items()) if len(s) >= 2]


def part1(lines: list[str]) -> list[str]:
    return [compress(ln) for ln in lines]


def part2(lines: list[str]) -> list[str]:
    return [compress(u.strip(), int(m)) for u, m in (ln.rsplit(",", 1) for ln in lines)]


def part3(lines: list[str]) -> list[str]:
    return [compress(u.strip(), None, int(n)) for u, n in (ln.rsplit(",", 1) for ln in lines)]


def part4(lines: list[str]) -> list[str]:
    return ambiguous(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
