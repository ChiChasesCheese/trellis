"""pc29 Valid Tic-Tac-Toe (Extended) -- YOUR implementation. Run the tests against this file with
IMPL=starter.

N x N board, K in a row (row/col/diag/anti-diag) wins. X first, alternating, game stops on a win.
Determine whether a board is reachable.

IMPORTANT subtlety (see problem.md): a player can have multiple simultaneous winning lines only
if ALL of them share one common cell -- checking that lines are merely pairwise-intersecting is
NOT enough once a player can have 3+ lines (two lines can each intersect a third without all
three sharing one cell). Verify against `enumerate_reachable_boards` (brute force) before trusting
your condition.
"""

from __future__ import annotations

import sys


def valid_tic_tac_toe(board: list[str]) -> bool:
    """Part1: LC 794 rules, 3x3, K=3."""
    # TODO
    return False


def valid_tic_tac_toe_nk(board: list[str], n: int, k: int) -> bool:
    """Part2: general N x N board, K in a row."""
    # TODO
    return False


def valid_tic_tac_toe_reason(board: list[str], n: int, k: int) -> str:
    """Part3 (reconstructed): 'OK', 'COUNT', 'BOTH_WIN', 'X_WIN_BAD_COUNT', 'O_WIN_BAD_COUNT',
    or 'DOUBLE_WIN_IMPOSSIBLE'."""
    # TODO
    return "OK"


def enumerate_reachable_boards(n: int, k: int, max_moves: int | None = None) -> set[tuple[str, ...]]:
    """Ground truth used only by tests: BFS over all legal games, collecting every board state
    ever seen. Exponential; only usable for small n. Provided as scaffolding -- you may reuse this
    verbatim, it isn't part of what's being graded."""
    def winning_lines(board_list, n, k, mark):
        lines = []
        def ok(cells):
            return all(board_list[r][c] == mark for r, c in cells)
        for r in range(n):
            for c in range(n - k + 1):
                cells = [(r, c + i) for i in range(k)]
                if ok(cells):
                    lines.append(cells)
        for c in range(n):
            for r in range(n - k + 1):
                cells = [(r + i, c) for i in range(k)]
                if ok(cells):
                    lines.append(cells)
        for r in range(n - k + 1):
            for c in range(n - k + 1):
                cells = [(r + i, c + i) for i in range(k)]
                if ok(cells):
                    lines.append(cells)
        for r in range(n - k + 1):
            for c in range(k - 1, n):
                cells = [(r + i, c - i) for i in range(k)]
                if ok(cells):
                    lines.append(cells)
        return lines

    start = tuple("".join("." for _ in range(n)) for _ in range(n))
    seen = {start}
    frontier = [start]
    moves = 0
    while frontier and (max_moves is None or moves < max_moves):
        moves += 1
        next_frontier = []
        mark = "X" if moves % 2 == 1 else "O"
        for board in frontier:
            board_list = list(board)
            if winning_lines(board_list, n, k, "X") or winning_lines(board_list, n, k, "O"):
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


def _read_board(lines: list[str], idx: int, n: int) -> tuple[list[str], int]:
    board = [lines[idx + i].replace("_", " ") for i in range(n)]
    return board, idx + n


def part1(lines: list[str]) -> list[str]:
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
