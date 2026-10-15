"""LC 179 Largest Number -- sort by the pairwise rule a+b > b+a (an exchange argument). Time O(n log n * L)."""
from functools import cmp_to_key
from itertools import permutations
from random import Random

# --- solution ---
def largest_number(nums):
    strs = [str(x) for x in nums]

    def cmp(a, b):                             # a goes first iff the concatenation a+b is larger
        return -1 if a + b > b + a else (1 if a + b < b + a else 0)

    strs.sort(key=cmp_to_key(cmp))
    out = "".join(strs)
    return "0" if out[0] == "0" else out       # [0, 0] must give "0", not "00"
# --- end ---

def _brute(nums):
    return str(max(int("".join(map(str, p))) for p in permutations(nums)))

if __name__ == "__main__":
    assert largest_number([10, 2]) == "210"
    assert largest_number([3, 30, 34, 5, 9]) == "9534330"
    assert largest_number([0, 0]) == "0"
    assert largest_number([1]) == "1"
    assert largest_number([121, 12]) == "12121"
    rng = Random(4)
    for _ in range(400):
        a = [rng.choice([0, 1, 2, 3, 9, 10, 12, 121, 34, 30, 5, 99, 100]) for _ in range(rng.randint(1, 6))]
        assert largest_number(a) == _brute(a), a
    print("ok 179_largest_number")
