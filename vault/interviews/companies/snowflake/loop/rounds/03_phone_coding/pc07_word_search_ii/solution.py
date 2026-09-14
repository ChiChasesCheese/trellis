"""pc07 Word Search II -- reference solution.

Part1 is LC 212 exactly: board of lowercase letters, list of words, return every word that can be
traced as a path of adjacent (up/down/left/right, no diagonals) cells without reusing a cell twice
in the same word. LC does not mandate an output order; we sort ascending for a deterministic
contract.

Part2 (reconstructed): for every found word also return its FIRST path, where "first" is defined
by two fixed traversal orders so the answer is reproducible:
  - start cells are tried in row-major order: (0,0), (0,1), ..., (0,C-1), (1,0), ...
  - from a cell, neighbours are tried in the fixed order UP, DOWN, LEFT, RIGHT
The classic LC212 trie is built once from all target words; each DFS step follows a trie edge, so
branches that cannot possibly complete a word are cut immediately. After a word's first path is
recorded we clear its terminal marker and prune any trie node left with no children and no word --
the standard optimization that keeps 3*10^4-word boards fast (dead branches stop being visited by
every subsequent DFS call).
"""

from __future__ import annotations

import sys

DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))  # UP, DOWN, LEFT, RIGHT -- fixes "first path"


class _Node:
    __slots__ = ("children", "word")

    def __init__(self) -> None:
        self.children: dict[str, "_Node"] = {}
        self.word: str | None = None


def _validate_board(board: list[list[str]]) -> None:
    if not board or not board[0]:
        raise ValueError("board must be a non-empty rectangular grid")
    width = len(board[0])
    for row in board:
        if len(row) != width:
            raise ValueError("board rows must all have the same length")
        for ch in row:
            if not isinstance(ch, str) or len(ch) != 1 or not ("a" <= ch <= "z"):
                raise ValueError(f"board cells must be single lowercase letters, got {ch!r}")


def _validate_words(words: list[str]) -> None:
    for w in words:
        if not w or not all("a" <= ch <= "z" for ch in w):
            raise ValueError(f"words must be non-empty lowercase strings, got {w!r}")


def _build_trie(words) -> _Node:
    root = _Node()
    for w in words:
        node = root
        for ch in w:
            node = node.children.setdefault(ch, _Node())
        node.word = w
    return root


def _search(board: list[list[str]], root: _Node) -> list[tuple[str, list[tuple[int, int]]]]:
    """DFS every start cell in row-major order; neighbours in DIRS order. Mutates `board` with a
    '#' sentinel while a cell is on the current path and always restores it before returning."""
    rows, cols = len(board), len(board[0])
    found: list[tuple[str, list[tuple[int, int]]]] = []
    path: list[tuple[int, int]] = []

    def dfs(r: int, c: int, node: _Node) -> None:
        ch = board[r][c]
        nxt = node.children.get(ch)
        if nxt is None:
            return
        path.append((r, c))
        board[r][c] = "#"
        if nxt.word is not None:
            found.append((nxt.word, list(path)))
            nxt.word = None  # first path only -- also unlocks pruning below
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                dfs(nr, nc, nxt)
        board[r][c] = ch
        path.pop()
        if not nxt.children and nxt.word is None:
            del node.children[ch]  # dead branch: never visited again

    for r in range(rows):
        for c in range(cols):
            if board[r][c] in root.children:
                dfs(r, c, root)
    return found


# --------------------------------------------------------------------------- Part 1
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    _validate_board(board)
    _validate_words(words)
    if not words:
        return []
    root = _build_trie(set(words))
    found = _search(board, root)
    return sorted(w for w, _ in found)


# --------------------------------------------------------------------------- Part 2
def find_words_with_paths(
    board: list[list[str]], words: list[str]
) -> list[tuple[str, list[tuple[int, int]]]]:
    _validate_board(board)
    _validate_words(words)
    if not words:
        return []
    root = _build_trie(set(words))
    found = _search(board, root)
    return sorted(found, key=lambda pair: pair[0])


# --------------------------------------------------------------------------- line-driven wrappers
def _read_board(lines: list[str], idx: int) -> tuple[list[list[str]], int]:
    r, c = map(int, lines[idx].split())
    idx += 1
    board = [list(lines[idx + t]) for t in range(r)]
    if any(len(row) != c for row in board):
        raise ValueError("declared width does not match a board row")
    return board, idx + r


def _read_words(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, k = lines[idx].split()
    if tag != "W":
        raise ValueError(f"expected 'W <k>', got {lines[idx]!r}")
    idx += 1
    k = int(k)
    return lines[idx : idx + k], idx + k


def part1(lines: list[str]) -> list[str]:
    """'R C' / R board rows / 'W k' / k words -> one line: found words asc, space-separated, or '-'."""
    board, idx = _read_board(lines, 0)
    words, _ = _read_words(lines, idx)
    found = find_words(board, words)
    return [" ".join(found) if found else "-"]


def part2(lines: list[str]) -> list[str]:
    """Same input -> one line per found word (asc): 'word r,c r,c ...'; '-' if none found."""
    board, idx = _read_board(lines, 0)
    words, _ = _read_words(lines, idx)
    pairs = find_words_with_paths(board, words)
    if not pairs:
        return ["-"]
    return [w + " " + " ".join(f"{r},{c}" for r, c in path) for w, path in pairs]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
