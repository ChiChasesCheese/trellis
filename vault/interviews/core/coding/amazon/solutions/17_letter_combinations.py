"""LC 17 Letter Combinations of a Phone Number -- backtracking, one digit per level. Time O(4^n * n)."""
from itertools import product

# --- solution ---
PHONE = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}

def letter_combinations(digits):
    if not digits:
        return []                            # NOT [""]: LeetCode defines the empty input as "no combinations"
    out, path = [], []

    def go(i):
        if i == len(digits):
            out.append("".join(path))
            return
        for ch in PHONE[digits[i]]:
            path.append(ch)
            go(i + 1)
            path.pop()

    go(0)
    return out
# --- end ---

def _brute(digits):
    if not digits:
        return []
    return ["".join(t) for t in product(*(PHONE[d] for d in digits))]

if __name__ == "__main__":
    assert letter_combinations("") == []
    assert letter_combinations("2") == ["a", "b", "c"]
    assert letter_combinations("23") == ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    for digits in ["7", "79", "234", "2222", "9876", "5"]:
        assert letter_combinations(digits) == _brute(digits), digits
    assert len(letter_combinations("7979")) == 4 ** 4
    print("ok 17_letter_combinations")
