"""LC 130 Surrounded Regions -- union every border 'O' with a dummy node; the 'O's not connected to it get flipped."""
from random import Random

# --- solution ---
def solve(board):
    """Flips surrounded 'O' to 'X' IN PLACE (the LeetCode contract); returns None."""
    if not board or not board[0]:
        return
    rows, cols = len(board), len(board[0])
    parent = list(range(rows * cols + 1))
    border = rows * cols                                   # dummy node = "connected to the outside"

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != "O":
                continue
            if r in (0, rows - 1) or c in (0, cols - 1):
                union(r * cols + c, border)
            for dr, dc in ((1, 0), (0, 1)):                # right and down are enough: every pair is seen once
                nr, nc = r + dr, c + dc
                if nr < rows and nc < cols and board[nr][nc] == "O":
                    union(r * cols + c, nr * cols + nc)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "O" and find(r * cols + c) != find(border):
                board[r][c] = "X"
# --- end ---

def _brute(board):
    rows, cols = len(board), len(board[0])
    safe, stack = set(), [(r, c) for r in range(rows) for c in range(cols)
                          if board[r][c] == "O" and (r in (0, rows - 1) or c in (0, cols - 1))]
    safe.update(stack)
    while stack:
        r, c = stack.pop()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "O" and (nr, nc) not in safe:
                safe.add((nr, nc))
                stack.append((nr, nc))
    return [["O" if (r, c) in safe else "X" if board[r][c] == "O" else board[r][c] for c in range(cols)] for r in range(rows)]

if __name__ == "__main__":
    b = [list("XXXX"), list("XOOX"), list("XXOX"), list("XOXX")]
    solve(b)
    assert b == [list("XXXX"), list("XXXX"), list("XXXX"), list("XOXX")]
    b = [["X"]]
    solve(b)
    assert b == [["X"]]
    b = [["O"]]
    solve(b)
    assert b == [["O"]]
    solve([])
    rng = Random(43)
    for _ in range(400):
        r, c = rng.randint(1, 6), rng.randint(1, 6)
        board = [[rng.choice("XO") for _ in range(c)] for _ in range(r)]
        want = _brute(board)
        solve(board)
        assert board == want, want
    print("ok 130_surrounded_regions")
