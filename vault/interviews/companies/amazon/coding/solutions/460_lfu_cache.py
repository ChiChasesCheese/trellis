"""LFU Cache (LC 460) -- key->(value,freq) plus freq->OrderedDict of keys (LRU inside a frequency); O(1) get/put."""
from collections import OrderedDict, defaultdict
from random import Random

# --- solution ---
class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.vals = {}                              # key -> value
        self.freq = {}                              # key -> use count
        self.buckets = defaultdict(OrderedDict)     # count -> keys with that count, oldest first
        self.min_freq = 0

    def _touch(self, key):
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:                  # the min bucket emptied: the key moves up to f+1
                self.min_freq = f + 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key):
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
        if len(self.vals) == self.cap:
            old, _ = self.buckets[self.min_freq].popitem(last=False)   # LFU, ties -> least recent
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.vals[old], self.freq[old]
        self.vals[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1                           # a brand-new key always has the minimum count
# --- end ---

class _Ref:                                         # O(n) reference: scan for (freq, last_used) minimum
    def __init__(self, cap):
        self.cap, self.d, self.t = cap, {}, 0

    def get(self, k):
        self.t += 1
        if k not in self.d:
            return -1
        v, f, _ = self.d[k]
        self.d[k] = (v, f + 1, self.t)
        return v

    def put(self, k, v):
        self.t += 1
        if self.cap == 0:
            return
        if k in self.d:
            self.d[k] = (v, self.d[k][1] + 1, self.t)
            return
        if len(self.d) == self.cap:
            victim = min(self.d, key=lambda x: (self.d[x][1], self.d[x][2]))
            del self.d[victim]
        self.d[k] = (v, 1, self.t)

if __name__ == "__main__":
    c = LFUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)                       # evicts 2 (count 1, older than 3)
    assert c.get(2) == -1
    assert c.get(3) == 3
    c.put(4, 4)                       # 1 and 3 both have count 2 -> evict the least recent, 1
    assert c.get(1) == -1 and c.get(3) == 3 and c.get(4) == 4
    z = LFUCache(0)
    z.put(1, 1)
    assert z.get(1) == -1
    rng = Random(23)
    for _ in range(150):
        cap = rng.randint(0, 4)
        a, b = LFUCache(cap), _Ref(cap)
        for _ in range(80):
            k = rng.randint(0, 5)
            if rng.random() < 0.5:
                v = rng.randint(0, 99)
                a.put(k, v)
                b.put(k, v)
            else:
                assert a.get(k) == b.get(k)
    print("ok 460_lfu_cache")
