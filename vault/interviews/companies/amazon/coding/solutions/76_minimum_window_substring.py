"""LC 76 Minimum Window Substring -- sliding window with a 'missing' counter. Time O(|s| + |t|), space O(alphabet)."""
from collections import Counter
from random import Random

# --- solution ---
def min_window(s, t):
    need = Counter(t)
    missing = len(t)                            # how many required chars are still uncovered
    best_l, best_len = 0, float("inf")
    left = 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1                           # may go negative: surplus copies
        if missing == 0:                        # window valid: shrink while it stays valid
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best_len:
                best_l, best_len = left, right - left + 1
            need[s[left]] += 1                  # drop s[left] to start looking for the next window
            missing += 1
            left += 1
    return "" if best_len == float("inf") else s[best_l:best_l + best_len]
# --- end ---

def _brute(s, t):
    best = ""
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            if not (Counter(t) - Counter(s[i:j])) and (not best or j - i < len(best)):
                best = s[i:j]
    return best

if __name__ == "__main__":
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""            # needs two a's
    assert min_window("ab", "b") == "b"
    assert min_window("aa", "aa") == "aa"
    rng = Random(25)
    for _ in range(400):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 9)))
        t = "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
        got, want = min_window(s, t), _brute(s, t)
        assert len(got) == len(want), (s, t, got, want)
        assert not got or not (Counter(t) - Counter(got)), (s, t, got)
    print("ok 76_minimum_window_substring")
