"""LC 48 Rotate Image -- clockwise rotation in place = transpose, then reverse every row. O(n^2) time, O(1) space."""
from random import Random

# --- solution ---
def rotate(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):                      # transpose: swap across the main diagonal
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()                                  # mirror left <-> right


def rotate_by_cycles(matrix):                          # the "four cells at a time" version interviewers sometimes ask for
    n = len(matrix)
    for i in range(n // 2):
        for j in range(i, n - 1 - i):
            tmp = matrix[i][j]
            matrix[i][j] = matrix[n - 1 - j][i]                   # left   -> top
            matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j]   # bottom -> left
            matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i]   # right  -> bottom
            matrix[j][n - 1 - i] = tmp                            # top    -> right
# --- end ---

if __name__ == "__main__":
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate(m)
    assert m == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    m = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
    rotate(m)
    assert m == [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]
    m = [[1]]
    rotate(m)
    assert m == [[1]]
    rng = Random(73)
    for _ in range(200):
        n = rng.randint(1, 8)
        m = [[rng.randint(0, 99) for _ in range(n)] for _ in range(n)]
        want = [list(row) for row in zip(*m[::-1])]      # the allocating one-liner
        a = [row[:] for row in m]
        b = [row[:] for row in m]
        rotate(a)
        rotate_by_cycles(b)
        assert a == want and b == want
        for _ in range(3):                                # four rotations are the identity
            rotate(a)
        assert a == m
    print("ok 48_rotate_image")
