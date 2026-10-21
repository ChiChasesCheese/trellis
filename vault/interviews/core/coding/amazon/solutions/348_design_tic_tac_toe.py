"""LC 348 Design Tic-Tac-Toe -- per-line counters (+1 / -1 per player): move() is O(1), memory O(n) instead of O(n^2)."""
from random import Random

# --- solution ---
class TicTacToe:
    def __init__(self, n):
        self.n = n
        self.rows = [0] * n
        self.cols = [0] * n
        self.diag = 0                                   # cells with row == col
        self.anti = 0                                   # cells with row + col == n - 1

    def move(self, row, col, player):
        """Returns the winning player (1 or 2) if this move completes a line, else 0. Assumes a legal move."""
        delta = 1 if player == 1 else -1                # a full line of one player has |count| == n
        n = self.n
        self.rows[row] += delta
        self.cols[col] += delta
        won = abs(self.rows[row]) == n or abs(self.cols[col]) == n
        if row == col:
            self.diag += delta
            won = won or abs(self.diag) == n            # look at a diagonal only if THIS move is on it
        if row + col == n - 1:
            self.anti += delta
            won = won or abs(self.anti) == n
        return player if won else 0
# --- end ---

def _line_complete(board, n, r, c, p):
    return (all(board[r][j] == p for j in range(n)) or all(board[i][c] == p for i in range(n))
            or (r == c and all(board[i][i] == p for i in range(n)))
            or (r + c == n - 1 and all(board[i][n - 1 - i] == p for i in range(n))))

if __name__ == "__main__":
    t = TicTacToe(3)
    assert [t.move(0, 0, 1), t.move(0, 2, 2), t.move(2, 2, 1), t.move(1, 1, 2), t.move(2, 0, 1), t.move(1, 0, 2), t.move(2, 1, 1)] == [0, 0, 0, 0, 0, 0, 1]
    t = TicTacToe(1)
    assert t.move(0, 0, 2) == 2
    t = TicTacToe(2)
    assert [t.move(0, 0, 1), t.move(1, 1, 1)] == [0, 1]                  # main diagonal
    t = TicTacToe(2)
    assert [t.move(0, 1, 2), t.move(1, 0, 2)] == [0, 2]                  # anti-diagonal
    rng = Random(89)
    for _ in range(300):
        n = rng.randint(1, 5)
        cells = [(r, c) for r in range(n) for c in range(n)]
        rng.shuffle(cells)
        game, board = TicTacToe(n), [[0] * n for _ in range(n)]
        for k, (r, c) in enumerate(cells):
            p = 1 + k % 2
            board[r][c] = p
            assert game.move(r, c, p) == (p if _line_complete(board, n, r, c, p) else 0)
    print("ok 348_design_tic_tac_toe")
