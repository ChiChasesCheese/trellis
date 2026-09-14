"""od13 Dictionary Trie Codec -- reference solution.

Source (MED, TrueInterview via kevin-2023-code/Tech-Interview-Questions "Serialize and
Deserialize Dictionary Trie", Algo, reported 2025-12): the confirmed shape is "distinct lowercase
words build a trie; serialize/deserialize it, deserialize returns all words in lexicographic
order". The encoding scheme, its compactness bound, malformed-input rejection, and the streaming
starts_with() are all reconstructed and stated in problem.md.

Encoding grammar (every character is one of '0', '1', '#', or a lowercase letter -- no escaping
needed because words never contain digits or '#'):

    node    ::= flag (letter node)* '#'
    flag    ::= '0' | '1'      -- '1' means this node's prefix-so-far is a complete word

Each node contributes exactly 2 non-letter characters (its own flag and its closing '#'); each
edge contributes exactly 1 letter character. So len(encoding) == 2*num_nodes + num_edges, and
num_edges == num_nodes - 1 (a trie is a tree), giving len(encoding) == 3*num_nodes - 1. Since the
sum of word lengths is always >= num_edges (every edge is walked by at least one word), this is
<= sum(len(w) for w in words) + 2*num_nodes -- the bound Part2's tests check.

Part1: build a trie (plain nested dict, no recursion needed to build it), serialize it, and
deserialize it back to the sorted list of words.
Part2: same encoding; tests check the length bound above and a perf/depth stress (word length up
to 10**4).
Part3: deserialize() rejects any input that doesn't match the grammar with ValueError (bad flag
character, dangling edge letter with no following node, unbalanced '#', trailing garbage after
the root closes); starts_with(data, prefix) answers a prefix query by scanning the encoded string
character-by-character, WITHOUT building any trie object -- it walks only the path that could
match the prefix and skips non-matching sibling subtrees using a constant-space bracket-depth
counter (flags open a node, '#' closes one; letters never change the nesting depth).
"""

from __future__ import annotations

import sys

_LOWER = frozenset("abcdefghijklmnopqrstuvwxyz")


# --------------------------------------------------------------------------- Part 1: build + serialize
def _build_trie(words: list[str]) -> dict:
    """node = {'word': bool, 'children': {letter: node}}. Iterative construction (a simple walk
    per word, no recursion)."""
    root: dict = {"word": False, "children": {}}
    for word in words:
        for ch in word:
            if ch not in _LOWER:
                raise ValueError(f"word must contain only lowercase letters a-z: {word!r}")
        node = root
        for ch in word:
            node = node["children"].setdefault(ch, {"word": False, "children": {}})
        node["word"] = True
    return root


def serialize(words: list[str]) -> str:
    """Iterative pre-order emission over an explicit stack of [node, sorted_letters, next_idx]
    frames -- no Python recursion, so arbitrarily long words (deep chains) never risk
    RecursionError. Encoding grammar documented at module top."""
    root = _build_trie(words)
    out: list[str] = ["1" if root["word"] else "0"]
    stack = [[root, sorted(root["children"]), 0]]
    while stack:
        frame = stack[-1]
        node, letters, idx = frame
        if idx < len(letters):
            letter = letters[idx]
            frame[2] += 1
            child = node["children"][letter]
            out.append(letter)
            out.append("1" if child["word"] else "0")
            stack.append([child, sorted(child["children"]), 0])
        else:
            out.append("#")
            stack.pop()
    return "".join(out)


def _skip_node(data: str, i: int) -> int:
    """i points at the flag digit that opens a node; returns the index just past its matching
    '#'. O(size of the skipped subtree), O(1) extra memory: flags ('0'/'1') open a node, '#'
    closes one, letters never change the depth -- so this is exactly balanced-bracket matching."""
    n = len(data)
    depth = 0
    while i < n:
        c = data[i]
        if c == "0" or c == "1":
            depth += 1
        elif c == "#":
            depth -= 1
            if depth == 0:
                return i + 1
        elif c not in _LOWER:
            raise ValueError(f"unexpected character {c!r} at position {i}")
        i += 1
    raise ValueError("unterminated node: reached end of data before matching '#'")


def deserialize(data: str) -> list[str]:
    """Iterative recursive-descent parse using an explicit stack of open nodes' prefixes (no
    Python recursion -- a word of length 10**4 pushes 10**4 stack frames onto a plain Python
    list, never onto the call stack). Rejects any malformed input with ValueError. Returns all
    words in lexicographic order."""
    if not data:
        raise ValueError("empty data")
    n = len(data)
    flag = data[0]
    if flag not in "01":
        raise ValueError(f"expected root flag '0'/'1', got {flag!r}")
    words: list[str] = [""] if flag == "1" else []
    stack: list[str] = [""]  # prefixes of nodes whose children list is still being read
    i = 1
    while stack:
        if i >= n:
            raise ValueError("unterminated node: reached end of data before matching '#'")
        c = data[i]
        if c == "#":
            i += 1
            stack.pop()
            continue
        if c not in _LOWER:
            raise ValueError(f"unexpected character {c!r} at position {i}")
        letter = c
        i += 1
        if i >= n or data[i] not in "01":
            got = data[i] if i < n else "<end of data>"
            raise ValueError(f"expected node flag after edge {letter!r}, got {got!r}")
        child_flag = data[i]
        i += 1
        child_prefix = stack[-1] + letter
        if child_flag == "1":
            words.append(child_prefix)
        stack.append(child_prefix)
    if i != n:
        raise ValueError(f"trailing data after root node closed: {data[i:]!r}")
    return sorted(words)


# --------------------------------------------------------------------------- Part 3: streaming query
def starts_with(data: str, prefix: str) -> bool:
    """True iff some word in the trie encoded by `data` has `prefix` as a prefix (the prefix
    itself need not be a complete word). Never builds a trie object: walks only the path that can
    match, skipping non-matching sibling subtrees with _skip_node(). Raises ValueError if the
    scanned portion of `data` is malformed, or if `prefix` contains a non-lowercase character."""
    if not data:
        raise ValueError("empty data")
    n = len(data)
    if data[0] not in "01":
        raise ValueError(f"expected root flag '0'/'1', got {data[0]!r}")
    i = 1
    for c in prefix:
        if c not in _LOWER:
            raise ValueError(f"prefix must be lowercase letters a-z: {c!r}")
        matched = False
        while i < n:
            ch = data[i]
            if ch == "#":
                break  # this node has no more children: prefix cannot continue
            if ch not in _LOWER:
                raise ValueError(f"unexpected character {ch!r} at position {i}")
            letter = ch
            i += 1
            if i >= n or data[i] not in "01":
                raise ValueError(f"expected node flag after edge {letter!r}")
            if letter == c:
                i += 1  # consume the matching child's flag; now inside its children list
                matched = True
                break
            i = _skip_node(data, i)  # not the letter we want: skip this whole child subtree
        if not matched:
            return False
    return True


# --------------------------------------------------------------------------- command stream
def _serialize_cmd(fields: list[str]) -> str:
    n = int(fields[1])
    words = fields[2 : 2 + n]
    return serialize(words)


def part1(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        fields = line.split()
        if fields[0] == "SERIALIZE":
            out.append(_serialize_cmd(fields))
        elif fields[0] == "DESERIALIZE":
            words = deserialize(fields[1])
            out.append(" ".join(words) if words else "-")
        else:
            raise ValueError(f"unknown command: {line!r}")
    return out


def part2(lines: list[str]) -> list[str]:
    return part1(lines)


def part3(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        fields = line.split()
        cmd = fields[0]
        if cmd == "SERIALIZE":
            out.append(_serialize_cmd(fields))
        elif cmd == "DESERIALIZE":
            try:
                words = deserialize(fields[1])
            except ValueError:
                out.append("ERROR")
            else:
                out.append(" ".join(words) if words else "-")
        elif cmd == "STARTSWITH":
            data = fields[1]
            prefix = fields[2] if len(fields) > 2 else ""
            try:
                result = starts_with(data, prefix)
            except ValueError:
                out.append("ERROR")
            else:
                out.append("true" if result else "false")
        else:
            raise ValueError(f"unknown command: {line!r}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
