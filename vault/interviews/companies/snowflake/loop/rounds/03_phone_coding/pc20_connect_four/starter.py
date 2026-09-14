"""pc20 Connect Four -- YOUR implementation. Run the tests against this file with IMPL=starter.

Board convention: `board` is a list of rows, board[0] is the TOP row, board[-1] is the BOTTOM
row; cells are "a", "b", or "" (empty). Coordinates are (x, y) = (row, col), 0-indexed.
"""

from __future__ import annotations

import sys


def can_play_win(board: list[list[str]], x: int, y: int, player: str) -> bool:
    """Part1: board[x][y] already equals `player`. Does this placement complete four-in-a-row
    (row, column, or either diagonal)? ValueError for a bad player / out-of-bounds coords /
    board[x][y] != player."""
    # TODO
    return False


def drop_and_check(board: list[list[str]], col: int, player: str) -> tuple[int, bool]:
    """Part2: drop `player`'s piece into `col` under gravity (mutates `board`). Returns
    (landed_row, is_win). ValueError if col is out of range or full."""
    # TODO
    return 0, False


class ConnectFour:
    """Part3: small OOD Connect Four. Turns alternate starting with 'a'; first four-in-a-row
    wins; a full board with no winner is a draw; drop() raises ValueError once the game is over
    or for an invalid column."""

    def __init__(self, rows: int = 6, cols: int = 7) -> None:
        # TODO
        pass

    def current_player(self) -> str:
        # TODO
        return "a"

    def winner(self) -> str | None:
        # TODO
        return None

    def is_draw(self) -> bool:
        # TODO
        return False

    def is_over(self) -> bool:
        # TODO
        return False

    def drop(self, col: int) -> int:
        # TODO
        return 0


def _parse_board(text: str) -> list[list[str]]:
    """rows separated by ';', cells separated by ',', '_' means empty."""
    return [["" if c == "_" else c for c in row.split(",")] for row in text.split(";")]


def part1(lines: list[str]) -> list[str]:
    """each line: 'board | x y player' -> 'true'/'false'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """each line: 'board | col player' -> 'row win_bool'."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """lines[0] = 'ROWS COLS'; each following line is a column index to drop into."""
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
