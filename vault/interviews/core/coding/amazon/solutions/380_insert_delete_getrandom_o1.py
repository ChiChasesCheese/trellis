"""LC 380 Insert Delete GetRandom O(1) -- list for random access + dict value->index; delete by swapping with last."""
import random
from collections import Counter

# --- solution ---
class RandomizedSet:
    def __init__(self):
        self.items = []
        self.pos = {}                          # value -> index in items

    def insert(self, val):
        if val in self.pos:
            return False
        self.pos[val] = len(self.items)
        self.items.append(val)
        return True

    def remove(self, val):
        if val not in self.pos:
            return False
        i = self.pos[val]
        last = self.items[-1]
        self.items[i] = last                   # overwrite the hole with the last element ...
        self.pos[last] = i
        self.items.pop()                       # ... then pop the tail in O(1)
        del self.pos[val]                      # delete AFTER the fix-up: val may itself be the last one
        return True

    def get_random(self):
        return random.choice(self.items)
# --- end ---

if __name__ == "__main__":
    s = RandomizedSet()
    assert s.insert(1) and not s.insert(1)
    assert s.remove(1) and not s.remove(1)
    assert s.insert(2) and s.insert(3) and s.insert(4)
    assert s.remove(2)                         # not last: swap path
    assert s.remove(4)                         # last: self-swap path
    assert sorted(s.items) == [3] and s.pos == {3: 0}
    assert s.get_random() == 3
    s = RandomizedSet()
    for v in range(5):
        s.insert(v)
    random.seed(0)
    counts = Counter(s.get_random() for _ in range(5000))
    assert set(counts) == set(range(5)) and min(counts.values()) > 800     # roughly uniform
    print("ok 380_insert_delete_getrandom_o1")
