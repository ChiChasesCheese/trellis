"""LC 79 Word Search -- DFS with in-place visited marks; prune by letter counts. Worst case O(R*C*3^L)."""
from collections import Counter
from random import Random

# --- solution ---
def exist(board, word):
    rows, cols = len(board), len(board[0])
    if len(word) > rows * cols:
        return False
    have = Counter(ch for row in board for ch in row)
    if any(have[ch] < need for ch, need in Counter(word).items()):
        return False                                       # cheap global prune: letters are missing
    if have[word[0]] > have[word[-1]]:
        word = word[::-1]                                  # start the DFS from the rarer end

    def dfs(r, c, i):
        if board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        saved, board[r][c] = board[r][c], None             # mark visited (None never equals a letter)
        found = False
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dfs(nr, nc, i + 1):
                found = True
                break
        board[r][c] = saved                                # un-choose BEFORE returning, on every path
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
# --- end ---

def _brute(board, word):
    rows, cols = len(board), len(board[0])
    def go(r, c, i, used):                                  # immutable visited set instead of marks
        if board[r][c] != word[i] or (r, c) in used:
            return False
        if i == len(word) - 1:
            return True
        used = used | {(r, c)}
        return any(go(r + dr, c + dc, i + 1, used)
                   for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if 0 <= r + dr < rows and 0 <= c + dc < cols)
    return any(go(r, c, 0, frozenset()) for r in range(rows) for c in range(cols))

if __name__ == "__main__":
    b = [list("ABCE"), list("SFCS"), list("ADEE")]
    assert exist(b, "ABCCED") is True
    assert exist(b, "SEE") is True
    assert exist(b, "ABCB") is False                       # would reuse the B
    assert b == [list("ABCE"), list("SFCS"), list("ADEE")]  # the board is restored
    assert exist([list("a")], "a") is True
    assert exist([list("a")], "aa") is False
    assert exist([list("aa")], "aaa") is False
    rng = Random(3)
    for _ in range(400):
        r, c = rng.randint(1, 4), rng.randint(1, 4)
        board = [[rng.choice("ab") for _ in range(c)] for _ in range(r)]
        word = "".join(rng.choice("ab") for _ in range(rng.randint(1, 7)))
        snap = [row[:] for row in board]
        assert exist(board, word) == _brute(snap, word), (snap, word)
        assert board == snap
    print("ok 79_word_search")
