"""LC 10 Regular Expression Matching ('.' and '*') -- 2D DP over (i, j) prefixes. Time O(m*n), space O(m*n)."""
import re
from random import Random

# --- solution ---
def is_match(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]     # dp[i][j]: s[:i] matches p[:j]
    dp[0][0] = True
    for j in range(2, n + 1):                          # empty s can match "a*b*" style prefixes
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                dp[i][j] = dp[i][j - 2]                # zero copies of the char before '*'
                if p[j - 2] in (s[i - 1], "."):
                    dp[i][j] = dp[i][j] or dp[i - 1][j]     # one more copy absorbs s[i-1]
            elif p[j - 1] in (s[i - 1], "."):
                dp[i][j] = dp[i - 1][j - 1]
    return dp[m][n]
# --- end ---

if __name__ == "__main__":
    assert not is_match("aa", "a")
    assert is_match("aa", "a*")
    assert is_match("ab", ".*")
    assert is_match("aab", "c*a*b")
    assert not is_match("mississippi", "mis*is*p*.")
    assert is_match("", "a*b*")
    assert not is_match("a", "")
    rng = Random(20)
    for _ in range(500):
        s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 6)))
        toks = []
        for _ in range(rng.randint(0, 4)):
            ch = rng.choice("ab.")
            toks.append(ch + ("*" if rng.random() < 0.4 else ""))
        p = "".join(toks)
        assert is_match(s, p) == bool(re.fullmatch(p, s)), (s, p)
    print("ok 10_regular_expression_matching")
