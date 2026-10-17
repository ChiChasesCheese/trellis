"""LC 51 N-Queens (+ LC 52 count) -- row-by-row backtracking with column / diagonal sets, then a bitmask version."""
from itertools import permutations

# --- solution ---
def solve_n_queens(n):
    boards, cols_of_row = [], []                 # cols_of_row[r] = column of the queen in row r
    cols, diag, anti = set(), set(), set()       # r - c is constant on "\" diagonals, r + c on "/" ones

    def go(r):
        if r == n:
            boards.append(["." * c + "Q" + "." * (n - c - 1) for c in cols_of_row])
            return
        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti:
                continue                          # attacked: prune the whole subtree
            cols.add(c); diag.add(r - c); anti.add(r + c)
            cols_of_row.append(c)
            go(r + 1)
            cols_of_row.pop()
            cols.remove(c); diag.remove(r - c); anti.remove(r + c)

    go(0)
    return boards


def total_n_queens(n):                            # LC 52: same search, three ints instead of three sets
    full = (1 << n) - 1

    def go(cols, diag, anti):
        if cols == full:
            return 1
        free = full & ~(cols | diag | anti)       # bit c set  <=>  column c is safe in this row
        count = 0
        while free:
            bit = free & -free                    # lowest safe column
            free ^= bit
            count += go(cols | bit, ((diag | bit) << 1) & full, (anti | bit) >> 1)
        return count

    return go(0, 0, 0)
# --- end ---

def _brute(n):
    out = []
    for perm in permutations(range(n)):           # one queen per row and column by construction
        if len({r + c for r, c in enumerate(perm)}) == n and len({r - c for r, c in enumerate(perm)}) == n:
            out.append(["." * c + "Q" + "." * (n - c - 1) for c in perm])
    return out

if __name__ == "__main__":
    assert solve_n_queens(1) == [["Q"]]
    assert solve_n_queens(2) == [] and solve_n_queens(3) == []
    assert sorted(solve_n_queens(4)) == [["..Q.", "Q...", "...Q", ".Q.."], [".Q..", "...Q", "Q...", "..Q."]]
    for n in range(1, 8):
        assert sorted(solve_n_queens(n)) == sorted(_brute(n)), n
    expected = [1, 0, 0, 2, 10, 4, 40, 92, 352, 724]
    for n in range(1, 11):
        assert total_n_queens(n) == expected[n - 1], n
    assert len(solve_n_queens(8)) == 92
    print("ok 51_n_queens")
