"""LC 54 Spiral Matrix -- four shrinking boundaries; the two guards inside the loop handle single rows / columns."""
from random import Random

# --- solution ---
def spiral_order(matrix):
    if not matrix or not matrix[0]:
        return []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):               # -> along the top row
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):               # v down the right column
            out.append(matrix[r][right])
        right -= 1
        if top <= bottom:                              # a single remaining row must not be walked back
            for c in range(right, left - 1, -1):       # <- along the bottom row
                out.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:                              # a single remaining column must not be walked back
            for r in range(bottom, top - 1, -1):       # ^ up the left column
                out.append(matrix[r][left])
            left += 1
    return out
# --- end ---

def _brute(matrix):
    if not matrix or not matrix[0]:
        return []
    rows, cols = len(matrix), len(matrix[0])
    seen = [[False] * cols for _ in range(rows)]
    r = c = d = 0
    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
    out = []
    for _ in range(rows * cols):
        out.append(matrix[r][c])
        seen[r][c] = True
        nr, nc = r + dirs[d][0], c + dirs[d][1]
        if not (0 <= nr < rows and 0 <= nc < cols) or seen[nr][nc]:
            d = (d + 1) % 4                              # turn right when blocked
            nr, nc = r + dirs[d][0], c + dirs[d][1]
        r, c = nr, nc
    return out

if __name__ == "__main__":
    assert spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    assert spiral_order([[1, 2, 3]]) == [1, 2, 3]
    assert spiral_order([[1], [2], [3]]) == [1, 2, 3]
    assert spiral_order([[1]]) == [1] and spiral_order([]) == [] and spiral_order([[]]) == []
    rng = Random(71)
    for _ in range(300):
        r, c = rng.randint(1, 7), rng.randint(1, 7)
        m = [[i * c + j for j in range(c)] for i in range(r)]
        assert spiral_order(m) == _brute(m), (r, c)
    print("ok 54_spiral_matrix")
