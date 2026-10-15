"""LC 146 LRU Cache -- hash map + doubly linked list with sentinels. get/put O(1)."""
from collections import OrderedDict
from random import Random

# --- solution ---
class _Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}                              # key -> node
        self.head, self.tail = _Node(), _Node()    # sentinels: most-recent side / least-recent side
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):                   # right after head = most recently used
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        node = self.map.get(key)
        if not node:
            return -1
        self._unlink(node)
        self._push_front(node)                     # reading makes it most recent
        return node.val

    def put(self, key, value):
        node = self.map.get(key)
        if node:
            node.val = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.cap:              # evict the least recently used = node before tail
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]                  # that's why the node stores its key
        node = _Node(key, value)
        self.map[key] = node
        self._push_front(node)
# --- end ---

class _Ref:                                        # OrderedDict reference model for the random test
    def __init__(self, cap):
        self.cap, self.d = cap, OrderedDict()

    def get(self, k):
        if k not in self.d:
            return -1
        self.d.move_to_end(k)
        return self.d[k]

    def put(self, k, v):
        if k in self.d:
            self.d.move_to_end(k)
        self.d[k] = v
        if len(self.d) > self.cap:
            self.d.popitem(last=False)

if __name__ == "__main__":
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)                       # evicts 2
    assert c.get(2) == -1
    c.put(4, 4)                       # evicts 1
    assert c.get(1) == -1 and c.get(3) == 3 and c.get(4) == 4
    one = LRUCache(1)
    one.put(1, 1)
    one.put(1, 9)                     # update, not insert: no eviction
    assert one.get(1) == 9
    one.put(2, 2)
    assert one.get(1) == -1 and one.get(2) == 2
    rng = Random(22)
    for _ in range(100):
        cap = rng.randint(1, 4)
        a, b = LRUCache(cap), _Ref(cap)
        for _ in range(60):
            k = rng.randint(0, 6)
            if rng.random() < 0.5:
                v = rng.randint(0, 99)
                a.put(k, v)
                b.put(k, v)
            else:
                assert a.get(k) == b.get(k)
    print("ok 146_lru_cache")
