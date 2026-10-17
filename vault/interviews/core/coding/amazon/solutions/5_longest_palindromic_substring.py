"""LC 5 Longest Palindromic Substring -- 2D table dp[i][j] (is s[i..j] a palindrome); O(n^2) time and space.
Alternative: expand around each center, O(n^2) time, O(1) space."""
from random import Random

# --- solution ---
def longest_palindrome(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]       # dp[i][j]: s[i..j] is a palindrome
    start, length = 0, 1
    for j in range(n):                         # right end outer, so dp[i+1][j-1] is already known
        for i in range(j + 1):
            if s[i] == s[j] and (j - i < 2 or dp[i + 1][j - 1]):
                dp[i][j] = True
                if j - i + 1 > length:
                    start, length = i, j - i + 1
    return s[start:start + length]


def longest_palindrome_expand(s):
    def grow(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return l + 1, r                        # bounds of the last valid palindrome
    best = (0, 1)
    for c in range(len(s)):
        for l, r in (grow(c, c), grow(c, c + 1)):     # odd and even centers
            if r - l > best[1] - best[0]:
                best = (l, r)
    return s[best[0]:best[1]]
# --- end ---

def _brute_len(s):
    return max((len(s[i:j]) for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1]), default=0)

if __name__ == "__main__":
    for f in (longest_palindrome, longest_palindrome_expand):
        assert f("babad") in ("bab", "aba")
        assert f("cbbd") == "bb"
        assert f("a") == "a"
        assert f("ac") in ("a", "c")
        assert f("aaaa") == "aaaa"
        rng = Random(19)
        for _ in range(200):
            s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 10)))
            r = f(s)
            assert r == r[::-1] and r in s and len(r) == _brute_len(s), s
    print("ok 5_longest_palindromic_substring")
