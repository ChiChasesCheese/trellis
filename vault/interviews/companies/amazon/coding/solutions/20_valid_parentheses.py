"""LC 20 Valid Parentheses -- stack of open brackets. Time O(n), space O(n)."""
# --- solution ---
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:                              # a closer: must match the latest opener
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack                                 # leftover openers -> invalid
# --- end ---

if __name__ == "__main__":
    assert is_valid("()[]{}")
    assert is_valid("{[]}")
    assert not is_valid("(]")
    assert not is_valid("([)]")
    assert not is_valid("(")              # leftover opener
    assert not is_valid(")")              # closer on empty stack
    assert is_valid("")
    print("ok 20_valid_parentheses")
