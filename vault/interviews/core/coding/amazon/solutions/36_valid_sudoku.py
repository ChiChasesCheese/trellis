"""LC 36 Valid Sudoku -- one pass, three bitmask arrays (row / column / box). O(81) = O(1) time."""
from random import Random

# --- solution ---
def is_valid_sudoku(board):
    rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9
    for r in range(9):
        for c in range(9):
            ch = board[r][c]
            if ch == ".":
                continue
            bit = 1 << (int(ch) - 1)
            b = r // 3 * 3 + c // 3                     # box index 0..8
            if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                return False                            # digit seen before in this row, column or box
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
    return True                                         # validity only: the puzzle may still be unsolvable
# --- end ---

def _brute(board):
    def ok(cells):
        digits = [x for x in cells if x != "."]
        return len(digits) == len(set(digits))
    return (all(ok(board[r]) for r in range(9))
            and all(ok([board[r][c] for r in range(9)]) for c in range(9))
            and all(ok([board[br + i][bc + j] for i in range(3) for j in range(3)]) for br in (0, 3, 6) for bc in (0, 3, 6)))

if __name__ == "__main__":
    good = ["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"]
    assert is_valid_sudoku([list(r) for r in good]) is True
    bad = [list(r) for r in good]
    bad[0][0] = "8"                                     # 8 twice in column 0 (and in the box)
    assert is_valid_sudoku(bad) is False
    bad = [list(r) for r in good]
    bad[1][2] = "3"                                     # 3 repeated inside the top-left box only (not its row/col)
    assert is_valid_sudoku(bad) is False and _brute(bad) is False
    rng = Random(79)
    for _ in range(600):
        b = [[rng.choice("..." + "123456789") for _ in range(9)] for _ in range(9)]
        for _ in range(rng.randint(0, 25)):
            b[rng.randrange(9)][rng.randrange(9)] = "."
        assert is_valid_sudoku(b) == _brute(b)
    print("ok 36_valid_sudoku")
