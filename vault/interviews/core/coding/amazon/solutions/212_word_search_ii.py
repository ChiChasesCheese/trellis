"""LC 212 Word Search II -- one DFS over the grid walking a trie of all words (instead of one DFS per word)."""
from random import Random

# --- solution ---
def find_words(board, words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w                                   # store the whole word at its end node: no path rebuilding
    rows, cols = len(board), len(board[0])
    found = []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent[ch]
        if "$" in node:
            found.append(node.pop("$"))                 # pop => each word is reported exactly once
        board[r][c] = None                              # mark visited
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node:
                dfs(nr, nc, node)
        board[r][c] = ch                                # un-choose
        if not node:
            del parent[ch]                              # prune: this branch has no unfound words left

    for r in range(rows):
        for c in range(cols):
            if board[r][c] in root:
                dfs(r, c, root)
    return found
# --- end ---

def _exist(board, word):
    rows, cols = len(board), len(board[0])
    def go(r, c, i, used):
        if board[r][c] != word[i] or (r, c) in used:
            return False
        if i == len(word) - 1:
            return True
        used = used | {(r, c)}
        return any(go(r + dr, c + dc, i + 1, used) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if 0 <= r + dr < rows and 0 <= c + dc < cols)
    return any(go(r, c, 0, frozenset()) for r in range(rows) for c in range(cols))

if __name__ == "__main__":
    b = [list("oaan"), list("etae"), list("ihkr"), list("iflv")]
    assert sorted(find_words(b, ["oath", "pea", "eat", "rain"])) == ["eat", "oath"]
    assert b == [list("oaan"), list("etae"), list("ihkr"), list("iflv")]
    assert find_words([list("ab"), list("cd")], ["abcb"]) == []
    assert find_words([list("a")], ["a", "a"]) == ["a"]               # duplicates in `words` reported once
    rng = Random(23)
    for _ in range(300):
        r, c = rng.randint(1, 4), rng.randint(1, 4)
        board = [[rng.choice("abc") for _ in range(c)] for _ in range(r)]
        words = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 5))) for _ in range(rng.randint(1, 8))]
        snap = [row[:] for row in board]
        got = find_words(board, words)
        assert sorted(got) == sorted({w for w in words if _exist(snap, w)}), (snap, words)
        assert board == snap and len(got) == len(set(got))
    print("ok 212_word_search_ii")
