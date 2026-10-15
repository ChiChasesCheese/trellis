"""LC 135 Candy -- two passes (left-to-right, right-to-left) take the max of both constraints. O(n) time."""
from random import Random

# --- solution ---
def candy(ratings):
    n = len(ratings)
    give = [1] * n                              # everyone gets at least one
    for i in range(1, n):                       # pass 1: satisfy "higher than the LEFT neighbour"
        if ratings[i] > ratings[i - 1]:
            give[i] = give[i - 1] + 1
    for i in range(n - 2, -1, -1):              # pass 2: satisfy "higher than the RIGHT neighbour"
        if ratings[i] > ratings[i + 1]:
            give[i] = max(give[i], give[i + 1] + 1)   # max keeps pass 1's result
    return sum(give)


def candy_o1(ratings):                          # one pass, O(1) extra space: count up-slopes and down-slopes
    n = len(ratings)
    total, up, down, peak = 1, 0, 0, 0
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            up += 1; peak = up; down = 0
            total += 1 + up
        elif ratings[i] == ratings[i - 1]:
            up = peak = down = 0
            total += 1
        else:
            up = 0; down += 1
            total += 1 + down - (1 if peak >= down else 0)   # a long enough descent must lift the peak by one
    return total
# --- end ---

def _brute(r):
    """Least fixed point: start with 1 each and keep raising until no rule is violated."""
    give = [1] * len(r)
    changed = True
    while changed:
        changed = False
        for i in range(len(r)):
            for j in (i - 1, i + 1):
                if 0 <= j < len(r) and r[i] > r[j] and give[i] <= give[j]:
                    give[i] = give[j] + 1
                    changed = True
    return sum(give)

if __name__ == "__main__":
    assert candy([1, 0, 2]) == 5
    assert candy([1, 2, 2]) == 4
    assert candy([1]) == 1
    assert candy([1, 2, 3, 4, 5]) == 15
    assert candy([5, 4, 3, 2, 1]) == 15
    rng = Random(6)
    for _ in range(800):
        r = [rng.randint(0, 4) for _ in range(rng.randint(1, 9))]
        want = _brute(r)
        assert candy(r) == want, r
        assert candy_o1(r) == want, r
    print("ok 135_candy")
