"""LC 3 Longest Substring Without Repeating Characters -- sliding window. Time O(n), space O(min(n, alphabet))."""
from random import Random

# --- solution ---
def length_of_longest_substring(s):
    last = {}                       # char -> most recent index
    left = 0                        # window is s[left..right]
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:   # duplicate INSIDE the window
            left = last[ch] + 1               # jump left just past the old copy
        last[ch] = right
        best = max(best, right - left + 1)
    return best
# --- end ---

def _brute(s):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            sub = s[i:j + 1]
            if len(set(sub)) == len(sub):
                best = max(best, len(sub))
    return best

if __name__ == "__main__":
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
    assert length_of_longest_substring("") == 0
    assert length_of_longest_substring("abba") == 2          # the classic left-moves-backwards bug
    rng = Random(1)
    for _ in range(300):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 10)))
        assert length_of_longest_substring(s) == _brute(s), s
    print("ok 3_longest_substring_without_repeating")
