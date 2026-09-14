"""q40 Query Words Within k — reference solution.

Document preprocesses word -> sorted positions once (the follow-up), so Part 1 is: for each
position i of the first query word, every other word needs an occurrence p with i < p <= i + k
(bisect_left(pos, i + 1)). Part 2 is a sliding window over the token list counting how many
distinct query words are inside; earliest start wins ties via strict '<'.
"""
from __future__ import annotations

import re
import sys
from bisect import bisect_left
from collections import defaultdict

WORD = re.compile(r"[a-z0-9]+")


def tokenize(text: str, normalize: bool = False) -> list[str]:
    return WORD.findall(text.lower()) if normalize else text.split()


class Document:
    def __init__(self, text: str, normalize: bool = False) -> None:
        self.tokens = tokenize(text, normalize)
        self.positions: dict[str, list[int]] = defaultdict(list)
        for i, w in enumerate(self.tokens):
            self.positions[w].append(i)


def _doc(text, normalize: bool) -> Document:
    return text if isinstance(text, Document) else Document(text, normalize)


def find_starts(text, query: str, k: int, normalize: bool = False) -> list[int]:
    doc = _doc(text, normalize)
    words = list(dict.fromkeys(tokenize(query, normalize)))   # dedupe, keep order
    if not words:
        return []
    first, others = words[0], words[1:]
    starts = []
    for i in doc.positions.get(first, []):
        ok = True
        for w in others:
            pos = doc.positions.get(w, [])
            j = bisect_left(pos, i + 1)                       # first occurrence strictly after i
            if j == len(pos) or pos[j] > i + k:               # must be <= i + k (inclusive)
                ok = False
                break
        if ok:
            starts.append(i)
    return starts


def min_window(text, query: str, normalize: bool = False) -> tuple[int, int] | None:
    doc = _doc(text, normalize)
    need = set(tokenize(query, normalize))
    if not need or any(w not in doc.positions for w in need):
        return None
    count: dict[str, int] = defaultdict(int)
    have, left, best = 0, 0, None
    for right, w in enumerate(doc.tokens):
        if w in need:
            count[w] += 1
            if count[w] == 1:
                have += 1
        while have == len(need):                               # shrink while still complete
            if best is None or right - left < best[1] - best[0]:  # strict '<': earliest on tie
                best = (left, right)
            lw = doc.tokens[left]
            if lw in need:
                count[lw] -= 1
                if count[lw] == 0:
                    have -= 1
            left += 1
    return best


def rank(docs: list[tuple[str, str]], query: str) -> list[tuple[str, int]]:
    scored = []
    for order, (name, text) in enumerate(docs):
        win = min_window(text, query, normalize=True)
        if win is not None:
            scored.append((win[1] - win[0] + 1, order, name))
    return [(name, length) for length, _, name in sorted(scored)]  # (length, input order)


def process(lines: list[str], part: int) -> list[str]:
    if part == 4:
        return [f"{n},{l}" for n, l in rank([tuple(ln.split("|", 1)) for ln in lines[1:]], lines[0])]
    doc = Document(lines[0], normalize=(part == 3))
    out = []
    for ln in lines[1:]:
        if part == 1:
            q, _, k = ln.rpartition("|")
            out.append(" ".join(map(str, find_starts(doc, q, int(k)))))
        else:
            win = min_window(doc, ln, normalize=(part == 3))
            out.append("-1" if win is None else f"{win[0]},{win[1]}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out = process(lines[1:], part)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
