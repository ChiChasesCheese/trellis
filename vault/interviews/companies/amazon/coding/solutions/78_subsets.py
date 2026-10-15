"""LC 78 Subsets (+ LC 90 with duplicates, LC 46 Permutations) -- one template, three pruning rules. 2^n subsets."""
from itertools import combinations, permutations
from random import Random

# --- solution ---
def subsets(nums):
    out, path = [], []

    def go(start):
        out.append(path[:])                   # every node of the recursion tree is an answer; COPY the path
        for i in range(start, len(nums)):
            path.append(nums[i])
            go(i + 1)                         # i + 1: each element used at most once, order fixed => no repeats
            path.pop()

    go(0)
    return out


def subsets_with_dup(nums):                   # LC 90: sort, then skip a value already tried at THIS level
    nums = sorted(nums)
    out, path = [], []

    def go(start):
        out.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            go(i + 1)
            path.pop()

    go(0)
    return out


def permutations_of(nums):                    # LC 46: "used" flags instead of a start index
    out, path, used = [], [], [False] * len(nums)

    def go():
        if len(path) == len(nums):
            out.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            go()
            path.pop()
            used[i] = False

    go()
    return out
# --- end ---

if __name__ == "__main__":
    assert subsets([]) == [[]]
    assert subsets([1, 2, 3]) == [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    assert sorted(subsets_with_dup([1, 2, 2])) == [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
    rng = Random(11)
    for _ in range(100):
        a = rng.sample(range(10), rng.randint(0, 7))
        mask = sorted(sorted(c) for r in range(len(a) + 1) for c in combinations(a, r))
        assert sorted(sorted(s) for s in subsets(a)) == mask
        assert len(subsets(a)) == 2 ** len(a)
        b = [rng.randint(0, 3) for _ in range(rng.randint(0, 7))]
        want = sorted({tuple(sorted(c)) for r in range(len(b) + 1) for c in combinations(sorted(b), r)})
        got = subsets_with_dup(b)
        assert sorted(tuple(s) for s in got) == want and len(got) == len(want)
        p = rng.sample(range(10), rng.randint(0, 6))
        assert sorted(permutations_of(p)) == sorted(list(t) for t in permutations(p))
    print("ok 78_subsets")
