"""pc29 Valid Tic-Tac-Toe (Extended, N x N, K in a row) -- reference solution.

Part1: the classic LC 794 rules on a 3x3, K=3 board.
Part2: generalise to N x N, K in a row (row/col/diag/anti-diag), same reachability rules.
Part3 (reconstructed): instead of True/False, return a reason code for WHY a board is invalid.

Reachability rules (LC 794, generalised):
- X always moves first, players alternate, so #X - #O is 0 or 1.
- Once a player has WON, the game stops -- no more moves are made. So:
  - if X has won, #X - #O must be exactly 1 (X's winning move was the last move, and O never
    got to move again).
  - if O has won, #X - #O must be exactly 0 (O's winning move was the last move; X and O have
    played the same number of moves).
  - a player cannot have TWO winning lines UNLESS they share the cell that was placed last --
    i.e. a single move completed two lines at once. We can't know which cell was "last", so we
    accept a double-win only if there EXISTS a cell shared by two of that player's winning lines
    (the move at that intersection could have completed both simultaneously); a player with two
    winning lines that share no common cell is unreachable (that would require two separate
    winning moves, but the game stops at the first one).
  - both players cannot have won (the game would have stopped at whichever happened first).
"""

from __future__ import annotations

import sys

# --------------------------------------------------------------------------- shared
def _winning_lines(board: list[str], n: int, k: int, mark: str) -> list[frozenset[tuple[int, int]]]:
    """All length-k runs of `mark` (row/col/diag/anti-diag) as sets of (r, c) cells."""
    lines: list[frozenset[tuple[int, int]]] = []

    def _cells_ok(cells: list[tuple[int, int]]) -> bool:
        return all(board[r][c] == mark for r, c in cells)

    for r in range(n):
        for c in range(n - k + 1):
            cells = [(r, c + i) for i in range(k)]
            if _cells_ok(cells):
                lines.append(frozenset(cells))
    for c in range(n):
        for r in range(n - k + 1):
            cells = [(r + i, c) for i in range(k)]
            if _cells_ok(cells):
                lines.append(frozenset(cells))
    for r in range(n - k + 1):
        for c in range(n - k + 1):
            cells = [(r + i, c + i) for i in range(k)]
            if _cells_ok(cells):
                lines.append(frozenset(cells))
    for r in range(n - k + 1):
        for c in range(k - 1, n):
            cells = [(r + i, c - i) for i in range(k)]
            if _cells_ok(cells):
                lines.append(frozenset(cells))
    return lines


def _reachable_reason(board: list[str], n: int, k: int) -> str:
    """Returns 'OK' if reachable, else one reason code:
    COUNT (bad #X/#O relationship), BOTH_WIN (both players have a winning line),
    X_WIN_BAD_COUNT (X has won but #X - #O != 1), O_WIN_BAD_COUNT (O has won but #X != #O),
    DOUBLE_WIN_IMPOSSIBLE (a player has two winning lines that share no common cell -- can't
    both have been completed by the same last move)."""
    if len(board) != n or any(len(row) != n for row in board):
        raise ValueError(f"board must be {n}x{n}")
    flat = "".join(board)
    x_count = flat.count("X")
    o_count = flat.count("O")
    if not (o_count == x_count or o_count == x_count - 1):
        return "COUNT"

    x_lines = _winning_lines(board, n, k, "X")
    o_lines = _winning_lines(board, n, k, "O")
    x_won, o_won = bool(x_lines), bool(o_lines)

    if x_won and o_won:
        return "BOTH_WIN"
    if x_won:
        if x_count - o_count != 1:
            return "X_WIN_BAD_COUNT"
        if len(x_lines) >= 2 and not _all_lines_share_a_common_cell(x_lines):
            return "DOUBLE_WIN_IMPOSSIBLE"
    if o_won:
        if x_count != o_count:
            return "O_WIN_BAD_COUNT"
        if len(o_lines) >= 2 and not _all_lines_share_a_common_cell(o_lines):
            return "DOUBLE_WIN_IMPOSSIBLE"
    return "OK"


def _all_lines_share_a_common_cell(lines: list[frozenset[tuple[int, int]]]) -> bool:
    """True iff there's a single cell present in EVERY winning line in `lines`. That's the exact
    condition for "the last move could have completed all of them at once": if some line omitted
    that cell, that line would already have been complete among the earlier moves, ending the
    game before the shared move -- so pairwise sharing is NOT enough when there are 3+ lines (two
    lines can each pairwise-intersect a third without all three sharing one common cell); we
    verified this the hard way, see problem.md and REPORT.md."""
    common = set(lines[0])
    for line in lines[1:]:
        common &= line
        if not common:
            return False
    return bool(common)


# --------------------------------------------------------------------------- Part 1
def valid_tic_tac_toe(board: list[str]) -> bool:
    """LC 794 rules: 3x3, K=3."""
    return _reachable_reason(board, 3, 3) == "OK"


# --------------------------------------------------------------------------- Part 2
def valid_tic_tac_toe_nk(board: list[str], n: int, k: int) -> bool:
    """General N x N board, K in a row."""
    return _reachable_reason(board, n, k) == "OK"


# --------------------------------------------------------------------------- Part 3
def valid_tic_tac_toe_reason(board: list[str], n: int, k: int) -> str:
    """(reconstructed) Same reachability check as Part2, but returns a reason code for an
    invalid board instead of just False: 'OK', 'COUNT', 'BOTH_WIN', 'X_WIN_BAD_COUNT',
    'O_WIN_BAD_COUNT', or 'DOUBLE_WIN_IMPOSSIBLE'."""
    return _reachable_reason(board, n, k)


# --------------------------------------------------------------------------- brute-force oracle
def enumerate_reachable_boards(n: int, k: int, max_moves: int | None = None) -> set[tuple[str, ...]]:
    """Ground truth used only by tests: BFS over all legal games (X first, alternating, stop the
    instant someone completes a k-in-a-row), collecting every board state ever seen (including
    mid-game states, not just terminal ones -- a board reachable mid-game is also "valid").
    Exponential; only usable for small n (3, maybe 4)."""
    start = tuple("".join("." for _ in range(n)) for _ in range(n))
    seen = {start}
    frontier = [start]
    moves = 0
    while frontier and (max_moves is None or moves < max_moves):
        moves += 1
        next_frontier = []
        turn_is_x = (moves % 2 == 1)
        mark = "X" if turn_is_x else "O"
        for board in frontier:
            board_list = list(board)
            # if this board is already a terminal win for either mark, no more moves happen from it
            if _winning_lines(board_list, n, k, "X") or _winning_lines(board_list, n, k, "O"):
                continue
            for r in range(n):
                for c in range(n):
                    if board_list[r][c] == ".":
                        new_row = board_list[r][:c] + mark + board_list[r][c + 1 :]
                        new_board = board_list[:r] + [new_row] + board_list[r + 1 :]
                        nb = tuple(new_board)
                        if nb not in seen:
                            seen.add(nb)
                            next_frontier.append(nb)
        frontier = next_frontier
    return seen


# --------------------------------------------------------------------------- line-driven wrappers
def _read_board(lines: list[str], idx: int, n: int) -> tuple[list[str], int]:
    board = [lines[idx + i].replace("_", " ") for i in range(n)]
    return board, idx + n


def part1(lines: list[str]) -> list[str]:
    """'N n' / n boards of 3 lines each (space cells written as '_') -> 'true'/'false' per board."""
    tag, count = lines[0].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[0]!r}")
    count = int(count)
    idx = 1
    out = []
    for _ in range(count):
        board, idx = _read_board(lines, idx, 3)
        out.append("true" if valid_tic_tac_toe(board) else "false")
    return out


def part2(lines: list[str]) -> list[str]:
    """'N n' / n blocks of 'SIZE n k' + n board lines -> 'true'/'false' per board."""
    tag, count = lines[0].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[0]!r}")
    count = int(count)
    idx = 1
    out = []
    for _ in range(count):
        size_tag, n_str, k_str = lines[idx].split()
        if size_tag != "SIZE":
            raise ValueError(f"expected 'SIZE n k', got {lines[idx]!r}")
        n, k = int(n_str), int(k_str)
        idx += 1
        board, idx = _read_board(lines, idx, n)
        out.append("true" if valid_tic_tac_toe_nk(board, n, k) else "false")
    return out


def part3(lines: list[str]) -> list[str]:
    """'N n' / n blocks of 'SIZE n k' + n board lines -> one reason code per board."""
    tag, count = lines[0].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[0]!r}")
    count = int(count)
    idx = 1
    out = []
    for _ in range(count):
        size_tag, n_str, k_str = lines[idx].split()
        if size_tag != "SIZE":
            raise ValueError(f"expected 'SIZE n k', got {lines[idx]!r}")
        n, k = int(n_str), int(k_str)
        idx += 1
        board, idx = _read_board(lines, idx, n)
        out.append(valid_tic_tac_toe_reason(board, n, k))
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
