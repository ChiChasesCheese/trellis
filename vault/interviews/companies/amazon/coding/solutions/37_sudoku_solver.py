"""LC 37 Sudoku Solver -- backtracking with bitmask candidates and the most-constrained-cell heuristic (MRV)."""
from random import Random

# --- solution ---
def solve_sudoku(board):
    """board: 9x9 list of lists of '1'..'9' or '.'; solved IN PLACE; returns True if a solution exists."""
    rows, cols, boxes, empties = [0] * 9, [0] * 9, [0] * 9, []
    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                empties.append((r, c))
            else:
                bit = 1 << (int(board[r][c]) - 1)
                rows[r] |= bit; cols[c] |= bit; boxes[r // 3 * 3 + c // 3] |= bit

    def solve(k):                                  # empties[:k] are filled; choose the next cell among empties[k:]
        if k == len(empties):
            return True
        best, best_mask, best_count = k, 0, 10
        for i in range(k, len(empties)):           # MRV: the cell with the fewest candidates fails fastest
            r, c = empties[i]
            mask = ~(rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3]) & 511
            count = bin(mask).count("1")
            if count < best_count:
                best, best_mask, best_count = i, mask, count
                if count <= 1:
                    break
        if best_count == 0:
            return False                           # dead end detected before branching
        empties[k], empties[best] = empties[best], empties[k]
        r, c = empties[k]
        b = r // 3 * 3 + c // 3
        mask = best_mask
        while mask:
            bit = mask & -mask
            mask ^= bit
            rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
            board[r][c] = str(bit.bit_length())
            if solve(k + 1):
                return True
            rows[r] ^= bit; cols[c] ^= bit; boxes[b] ^= bit
        board[r][c] = "."                          # un-choose the cell itself
        return False

    return solve(0)
# --- end ---

def _is_valid_full(board):
    want = set("123456789")
    return (all(set(row) == want for row in board)
            and all({board[r][c] for r in range(9)} == want for c in range(9))
            and all({board[br + i][bc + j] for i in range(3) for j in range(3)} == want
                    for br in (0, 3, 6) for bc in (0, 3, 6)))

if __name__ == "__main__":
    puzzle = ["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"]
    b = [list(r) for r in puzzle]
    assert solve_sudoku(b) is True
    assert ["".join(r) for r in b][0] == "534678912" and ["".join(r) for r in b][8] == "345286179"
    assert _is_valid_full(b)
    # a very hard 17-clue style puzzle (little information for naive row-by-row search)
    hard = ["8........", "..36.....", ".7..9.2..", ".5...7...", "....457..", "...1...3.", "..1....68", "..85...1.", ".9....4.."]
    h = [list(r) for r in hard]
    assert solve_sudoku(h) is True and _is_valid_full(h)
    for r in range(9):
        for c in range(9):
            if hard[r][c] != ".":
                assert h[r][c] == hard[r][c]            # clues untouched
    # random puzzles: take a solved grid, blank cells, solve again, must be valid and keep the clues
    rng = Random(5)
    full = [list(r) for r in ["." * 9] * 9]
    assert solve_sudoku(full) and _is_valid_full(full)
    for _ in range(20):
        p = [row[:] for row in full]
        for _ in range(rng.randint(30, 50)):
            p[rng.randrange(9)][rng.randrange(9)] = "."
        q = [row[:] for row in p]
        assert solve_sudoku(q) and _is_valid_full(q)
        assert all(p[r][c] in (".", q[r][c]) for r in range(9) for c in range(9))
    unsolvable = [list(r) for r in ["." * 9] * 9]
    unsolvable[0][0:8] = list("12345678")
    unsolvable[1][8] = "9"                             # cell (0,8) has no candidate left
    assert solve_sudoku(unsolvable) is False
    print("ok 37_sudoku_solver")
