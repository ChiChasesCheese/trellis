"""pc20 Connect Four -- reference solution.

Board convention (all three parts): `board` is a list of rows, `board[0]` is the TOP row,
`board[-1]` is the BOTTOM row; each cell is `"a"`, `"b"`, or `""` (empty). Coordinates are
`(x, y)` = `(row, col)`, both 0-indexed.

Part1 assumes the move has ALREADY been placed on the board (board[x][y] == player) and answers
"does this placement complete four-in-a-row?" by walking outward from (x, y) along each of the
four axes (horizontal, vertical, and both diagonals), counting consecutive same-player cells in
both directions of each axis and adding 1 for the placed cell itself.

Part2 (reconstructed) adds gravity: dropping into a column lands on the lowest empty row of that
column (row indices grow downward, so "lowest" = largest row index with an empty cell), then
reuses Part1's check on the landing square.

Part3 is the "Design Connect Four" LLD (TrueInterview #18, same family as #16's canPlayWin):
a small stateful class wrapping Part2's drop-and-check, tracking whose turn it is, the winner,
and draws, and rejecting moves once the game is decided or the target column is full/out of
range.
"""

from __future__ import annotations

import sys

_DIRECTIONS = (
    ((0, 1), (0, -1)),    # horizontal
    ((1, 0), (-1, 0)),    # vertical
    ((1, 1), (-1, -1)),   # diagonal '\'
    ((1, -1), (-1, 1)),   # diagonal '/'
)


def _check_player(player: str) -> None:
    if player not in ("a", "b"):
        raise ValueError(f"player must be 'a' or 'b', got {player!r}")


def _in_bounds(board: list[list[str]], x: int, y: int) -> bool:
    return 0 <= x < len(board) and 0 <= y < len(board[0])


# --------------------------------------------------------------------------- Part 1
def can_play_win(board: list[list[str]], x: int, y: int, player: str) -> bool:
    """board[x][y] must already equal `player` (the move has been placed). Returns True if that
    placement completes four (or more) in a row in any of the 4 axes."""
    _check_player(player)
    if not _in_bounds(board, x, y):
        raise ValueError(f"({x}, {y}) is out of bounds for a {len(board)}x{len(board[0])} board")
    if board[x][y] != player:
        raise ValueError(f"board[{x}][{y}] is {board[x][y]!r}, not the placed player {player!r}")

    for (dx1, dy1), (dx2, dy2) in _DIRECTIONS:
        count = 1
        cx, cy = x + dx1, y + dy1
        while _in_bounds(board, cx, cy) and board[cx][cy] == player:
            count += 1
            cx, cy = cx + dx1, cy + dy1
        cx, cy = x + dx2, y + dy2
        while _in_bounds(board, cx, cy) and board[cx][cy] == player:
            count += 1
            cx, cy = cx + dx2, cy + dy2
        if count >= 4:
            return True
    return False


# --------------------------------------------------------------------------- Part 2
def drop_and_check(board: list[list[str]], col: int, player: str) -> tuple[int, bool]:
    """Drop `player`'s piece into `col` (gravity: lands on the lowest empty row), mutating
    `board` in place. Returns (landed_row, is_win). ValueError if col is out of range or full."""
    _check_player(player)
    if not (0 <= col < len(board[0])):
        raise ValueError(f"col {col} out of range for a board with {len(board[0])} columns")
    landed_row = None
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == "":
            landed_row = row
            break
    if landed_row is None:
        raise ValueError(f"column {col} is full")
    board[landed_row][col] = player
    return landed_row, can_play_win(board, landed_row, col, player)


# --------------------------------------------------------------------------- Part 3
class ConnectFour:
    """Small OOD Connect Four: alternating turns starting with 'a', first four-in-a-row wins,
    a full board with no winner is a draw. Once the game is over (winner or draw), drop()
    raises ValueError."""

    def __init__(self, rows: int = 6, cols: int = 7) -> None:
        if rows < 4 or cols < 4:
            raise ValueError("Connect Four needs at least a 4x4 board")
        self._board: list[list[str]] = [["" for _ in range(cols)] for _ in range(rows)]
        self._turn = "a"
        self._winner: str | None = None
        self._moves_played = 0
        self._rows, self._cols = rows, cols

    def current_player(self) -> str:
        return self._turn

    def winner(self) -> str | None:
        return self._winner

    def is_draw(self) -> bool:
        return self._winner is None and self._moves_played == self._rows * self._cols

    def is_over(self) -> bool:
        return self._winner is not None or self.is_draw()

    def drop(self, col: int) -> int:
        """Drop the current player's piece into `col`. Returns the landed row. ValueError if
        the game is already over, or `col` is out of range / full."""
        if self.is_over():
            raise ValueError("game is already over")
        if not (0 <= col < self._cols):
            raise ValueError(f"col {col} out of range for a board with {self._cols} columns")
        player = self._turn
        landed_row, won = drop_and_check(self._board, col, player)
        self._moves_played += 1
        if won:
            self._winner = player
        # The turn always advances, even on a winning move -- current_player() then means "who
        # would move next", which stays well-defined whether or not the game just ended (once
        # ended, drop() simply refuses everyone, including this nominal next player).
        self._turn = "b" if player == "a" else "a"
        return landed_row


# --------------------------------------------------------------------------- line-driven wrappers
def _parse_board(text: str) -> list[list[str]]:
    """rows separated by ';', cells separated by ',', '_' means empty."""
    return [["" if c == "_" else c for c in row.split(",")] for row in text.split(";")]


def _format_board(board: list[list[str]]) -> str:
    return ";".join(",".join("_" if c == "" else c for c in row) for row in board)


def part1(lines: list[str]) -> list[str]:
    """each line: 'board | x y player' -> 'true'/'false'."""
    out = []
    for line in lines:
        left, right = line.split("|")
        board = _parse_board(left.strip())
        x_s, y_s, player = right.split()
        out.append("true" if can_play_win(board, int(x_s), int(y_s), player) else "false")
    return out


def part2(lines: list[str]) -> list[str]:
    """each line: 'board | col player' -> 'row win_bool' (win_bool is 'true'/'false')."""
    out = []
    for line in lines:
        left, right = line.split("|")
        board = _parse_board(left.strip())
        col_s, player = right.split()
        row, win = drop_and_check(board, int(col_s), player)
        out.append(f"{row} {'true' if win else 'false'}")
    return out


def part3(lines: list[str]) -> list[str]:
    """lines[0] = 'ROWS COLS'; each following line is a column index to drop into -> one output
    line per drop: 'row current_player winner_or_NONE draw_bool'."""
    rows, cols = map(int, lines[0].split())
    game = ConnectFour(rows, cols)
    out = []
    for line in lines[1:]:
        col = int(line)
        row = game.drop(col)
        out.append(
            f"{row} {game.current_player()} "
            f"{game.winner() if game.winner() else 'NONE'} "
            f"{'true' if game.is_draw() else 'false'}"
        )
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
