"""LC 22 Generate Parentheses -- backtracking with two counters. Output size is Catalan(n); time O(4^n / sqrt(n))."""
from itertools import product

# --- solution ---
def generate_parenthesis(n):
    out, path = [], []

    def go(opened, closed):
        if opened == n and closed == n:
            out.append("".join(path))
            return
        if opened < n:                       # may always open while we still have budget
            path.append("(")
            go(opened + 1, closed)
            path.pop()                       # un-choose
        if closed < opened:                  # may close only what is open: this prunes every invalid prefix
            path.append(")")
            go(opened, closed + 1)
            path.pop()

    go(0, 0)
    return out
# --- end ---

def _valid(s):
    depth = 0
    for ch in s:
        depth += 1 if ch == "(" else -1
        if depth < 0:
            return False
    return depth == 0

def _brute(n):
    return sorted("".join(t) for t in product("()", repeat=2 * n) if _valid("".join(t)))

if __name__ == "__main__":
    assert generate_parenthesis(0) == [""]
    assert generate_parenthesis(1) == ["()"]
    assert generate_parenthesis(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
    catalan = [1, 1, 2, 5, 14, 42, 132, 429, 1430]
    for n in range(9):
        got = generate_parenthesis(n)
        assert len(got) == catalan[n] and len(set(got)) == len(got)
    for n in range(6):
        assert sorted(generate_parenthesis(n)) == _brute(n), n
    print("ok 22_generate_parentheses")
