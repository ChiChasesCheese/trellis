"""LC 73 Set Matrix Zeroes -- use the first row and first column as the marker arrays: O(1) extra space."""
from random import Random

# --- solution ---
def set_zeroes(matrix):
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(cols))      # these two flags remember the markers' own state
    first_col_zero = any(matrix[r][0] == 0 for r in range(rows))
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][c] == 0:
                matrix[r][0] = matrix[0][c] = 0                       # mark row r and column c
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    if first_row_zero:                                                # LAST: the markers were still needed above
        for c in range(cols):
            matrix[0][c] = 0
    if first_col_zero:
        for r in range(rows):
            matrix[r][0] = 0
# --- end ---

def _brute(m):
    zr = {r for r, row in enumerate(m) for x in row if x == 0}
    zc = {c for row in m for c, x in enumerate(row) if x == 0}
    return [[0 if r in zr or c in zc else x for c, x in enumerate(row)] for r, row in enumerate(m)]

if __name__ == "__main__":
    m = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    set_zeroes(m)
    assert m == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    m = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
    set_zeroes(m)
    assert m == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
    m = [[1]]
    set_zeroes(m)
    assert m == [[1]]
    m = [[1, 0]]
    set_zeroes(m)
    assert m == [[0, 0]]
    rng = Random(83)
    for _ in range(600):
        r, c = rng.randint(1, 5), rng.randint(1, 5)
        m = [[rng.choice([0, 1, 1, 1, 2]) for _ in range(c)] for _ in range(r)]
        want = _brute(m)
        set_zeroes(m)
        assert m == want
    print("ok 73_set_matrix_zeroes")
