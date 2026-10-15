"""LC 139 Word Break -- forward DP over positions; a trie walk from each reachable position. O(n * L) time."""
from random import Random

# --- solution ---
def word_break(s, word_dict):
    root = {}
    for w in word_dict:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True                          # a dictionary word ends here
    n = len(s)
    reachable = [False] * (n + 1)                 # reachable[i]: s[:i] can be segmented
    reachable[0] = True
    for i in range(n):
        if not reachable[i]:
            continue
        node = root
        for j in range(i, n):                     # extend one character at a time, stop when no word continues
            node = node.get(s[j])
            if node is None:
                break
            if "$" in node:
                reachable[j + 1] = True
        if reachable[n]:
            return True
    return reachable[n]
# --- end ---

def _brute(s, words):
    ws = set(words)
    def go(i):
        return i == len(s) or any(s[i:j] in ws and go(j) for j in range(i + 1, len(s) + 1))
    return go(0)

if __name__ == "__main__":
    assert word_break("leetcode", ["leet", "code"]) is True
    assert word_break("applepenapple", ["apple", "pen"]) is True
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    assert word_break("", ["a"]) is True
    assert word_break("a", []) is False
    assert word_break("a" * 40 + "b", ["a", "aa", "aaa"]) is False      # exponential for the naive recursion
    rng = Random(21)
    for _ in range(600):
        words = ["".join(rng.choice("ab") for _ in range(rng.randint(1, 3))) for _ in range(rng.randint(0, 4))]
        s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 9)))
        assert word_break(s, words) == _brute(s, words), (s, words)
    print("ok 139_word_break")
