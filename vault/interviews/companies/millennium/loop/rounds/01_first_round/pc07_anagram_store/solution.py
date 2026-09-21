"""pc07 Anagram Store -- reference solution.

Warm-up (LC 20, Valid Parentheses): a stack of open brackets, pop-and-match on every closer --
included because StealthCoder's Millennium tag list reports this as a standalone easy alongside
the anagram-store design question, and it is a natural "prove you can code a stack" opener before
the design question.

Part1 (PracHub "Design a data structure to store anagrams"): AnagramStore groups words by a
canonical key. Two candidate keys are compared explicitly: `canonical_key_sorted` (sort the
characters, O(L log L), works for any alphabet including Unicode) and `canonical_key_counts`
(a 26-slot count vector, O(L), but only defined for lowercase a-z) -- the store itself always
uses the sorted key internally so it keeps working once Part3 lifts the a-z restriction.

Part2: `remove` deletes one exact-string occurrence from its group (not "any word with the same
canonical key" -- removal is by literal string identity, same as a real store where you hand back
the exact record you inserted). `most_common_group` breaks ties by the canonical key's own
lexicographic order, so the winner is deterministic regardless of insertion order.

Part3 (reconstructed): a `case_sensitive` policy on the store (case-fold with `str.casefold()`,
which is the Unicode-correct generalisation of `.lower()`, before computing the sorted key) plus
`top_k_groups`, a streaming top-k query that can be called after any sequence of `add`s.
"""

from __future__ import annotations

import sys

_OPENERS = {"(", "[", "{"}
_PAIRS = {")": "(", "]": "[", "}": "{"}


# --------------------------------------------------------------------------- warm-up
def is_valid_parentheses(s: str) -> bool:
    """LC 20. s must contain only bracket characters '()[]{}' -> ValueError otherwise."""
    if not isinstance(s, str):
        raise ValueError(f"s must be str, got {s!r}")
    for ch in s:
        if ch not in _OPENERS and ch not in _PAIRS:
            raise ValueError(f"s must contain only bracket characters, got {ch!r} in {s!r}")
    stack: list[str] = []
    for ch in s:
        if ch in _OPENERS:
            stack.append(ch)
        elif not stack or stack.pop() != _PAIRS[ch]:
            return False
    return not stack


# --------------------------------------------------------------------------- Part 1
def canonical_key_sorted(word: str) -> str:
    """O(L log L), works for any alphabet (including Unicode): sort the characters."""
    if not isinstance(word, str):
        raise ValueError(f"word must be str, got {word!r}")
    return "".join(sorted(word))


def canonical_key_counts(word: str) -> tuple[int, ...]:
    """O(L), but only defined for lowercase a-z: a 26-slot count vector. Any other character
    (uppercase, digit, punctuation, non-ASCII) -> ValueError, because the fixed-size vector has
    nowhere to put it."""
    if not isinstance(word, str):
        raise ValueError(f"word must be str, got {word!r}")
    counts = [0] * 26
    for ch in word:
        if not ("a" <= ch <= "z"):
            raise ValueError(f"canonical_key_counts only supports lowercase a-z, got {ch!r} in {word!r}")
        counts[ord(ch) - ord("a")] += 1
    return tuple(counts)


class AnagramStore:
    """Stores words, grouped by anagram. Group membership uses `canonical_key_sorted` internally
    (so it keeps working for Unicode / any-case input once `case_sensitive=False`); within a
    group, words are kept in insertion order and duplicates of the same literal string are
    allowed (each `add` appends one instance)."""

    def __init__(self, case_sensitive: bool = True) -> None:
        if not isinstance(case_sensitive, bool):
            raise ValueError(f"case_sensitive must be bool, got {case_sensitive!r}")
        self.case_sensitive = case_sensitive
        self._groups: dict[str, list[str]] = {}

    def _key(self, word: str) -> str:
        if not isinstance(word, str):
            raise ValueError(f"word must be str, got {word!r}")
        folded = word if self.case_sensitive else word.casefold()
        return canonical_key_sorted(folded)

    def add(self, word: str) -> None:
        key = self._key(word)
        self._groups.setdefault(key, []).append(word)

    def group_of(self, word: str) -> list[str]:
        """Words (insertion order) sharing `word`'s anagram group; [] if none (not an error --
        querying a word that was never added is a normal empty result)."""
        return list(self._groups.get(self._key(word), []))

    def count(self, word: str) -> int:
        return len(self.group_of(word))

    # ----------------------------------------------------------------------- Part 2
    def remove(self, word: str) -> None:
        """Remove ONE occurrence of the exact string `word` from its group (literal-string
        identity, not "any word with the same canonical key"). ValueError if that exact string
        is not currently in the store, even if other words in the same group are."""
        key = self._key(word)
        group = self._groups.get(key)
        if not group or word not in group:
            raise ValueError(f"{word!r} is not present in the store")
        group.remove(word)  # removes the first (oldest) occurrence
        if not group:
            del self._groups[key]

    def most_common_group(self) -> list[str]:
        """The group (insertion order) with the most members. Empty store -> [] (not an error).
        Tie-break: smallest canonical key, so the winner never depends on insertion order."""
        if not self._groups:
            return []
        best_key = min(self._groups, key=lambda k: (-len(self._groups[k]), k))
        return list(self._groups[best_key])

    # ----------------------------------------------------------------------- Part 3 (reconstructed)
    def top_k_groups(self, k: int) -> list[list[str]]:
        """The k largest groups, ranked by size desc then canonical key asc (same tie-break as
        `most_common_group`). k must be a positive int. Fewer than k groups exist -> returns all
        of them (not an error); an empty store -> []."""
        if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
            raise ValueError(f"k must be a positive int, got {k!r}")
        ranked = sorted(self._groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        return [list(words) for _, words in ranked[:k]]


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """ops: 'ADD <word>' (no output) / 'GROUP <word>' -> space-joined group / 'COUNT <word>' -> int."""
    store = AnagramStore()
    out: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        cmd, *rest = line.split()
        if cmd == "ADD":
            store.add(rest[0])
        elif cmd == "GROUP":
            out.append(" ".join(store.group_of(rest[0])))
        elif cmd == "COUNT":
            out.append(str(store.count(rest[0])))
        else:
            raise ValueError(f"unknown op {line!r}")
    return out


def part2(lines: list[str]) -> list[str]:
    """part1 ops plus 'REMOVE <word>' (no output) / 'MOSTCOMMON' -> space-joined group."""
    store = AnagramStore()
    out: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        cmd, *rest = line.split()
        if cmd == "ADD":
            store.add(rest[0])
        elif cmd == "GROUP":
            out.append(" ".join(store.group_of(rest[0])))
        elif cmd == "COUNT":
            out.append(str(store.count(rest[0])))
        elif cmd == "REMOVE":
            store.remove(rest[0])
        elif cmd == "MOSTCOMMON":
            out.append(" ".join(store.most_common_group()))
        else:
            raise ValueError(f"unknown op {line!r}")
    return out


def part3(lines: list[str]) -> list[str]:
    """lines[0] = 'CASE SENSITIVE' | 'CASE INSENSITIVE', then 'ADD <word>' (no output) /
    'TOPK <k>' -> groups joined by '|', each group's words joined by ' ' (empty line if no groups)."""
    if not lines or not lines[0].startswith("CASE "):
        raise ValueError("part3 input must start with 'CASE SENSITIVE' or 'CASE INSENSITIVE'")
    case_sensitive = lines[0].split()[1] == "SENSITIVE"
    store = AnagramStore(case_sensitive=case_sensitive)
    out: list[str] = []
    for line in lines[1:]:
        if not line.strip():
            continue
        cmd, *rest = line.split()
        if cmd == "ADD":
            store.add(rest[0])
        elif cmd == "TOPK":
            groups = store.top_k_groups(int(rest[0]))
            out.append("|".join(" ".join(g) for g in groups))
        else:
            raise ValueError(f"unknown op {line!r}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
