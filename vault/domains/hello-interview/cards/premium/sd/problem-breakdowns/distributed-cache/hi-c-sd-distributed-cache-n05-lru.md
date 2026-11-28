---
id: hi-c-sd-distributed-cache-n05-lru
node: sd.problem-breakdowns.distributed-cache.notes
type: qa
step: 5
---
## Q
**分布式缓存 · LRU：哈希表加双向链表**｜摘要 · 必会

为什么 LRU 要同时用哈希表和双向链表？get、set、淘汰怎么做到 O(1)？

## A
- **两难：** 只用哈希表，查找快但不知道谁最久没用；只用链表，知道顺序但查找要遍历。
- **合用：** 哈希表映射 key → 链表节点，链表按使用顺序排（表头最近、表尾最久）。
  - 访问：哈希表 O(1) 找到节点，从当前位置摘下（双向链表能在 O(1) 内删除）再插到表头；
  - 写入新键：建节点、放进哈希表、插到表头，超容量就删表尾那个节点，同时从哈希表里删；
  - 过期：节点里存 expiry，读到过期的同时从两处删除。
- **例：** 容量 2，依次加 A、B、C，结果是 [C → B]，A 被淘汰。
- **哨兵节点：** 用一个假的头（含尾）免去"空链表""只有一个节点"的特殊判断。
- **常见错误：** 删除只删了一边（哈希表和链表必须同步），一边留着就是内存泄漏或幽灵节点。

```python
import time

class Node:
    __slots__ = ("key", "value", "expiry", "prev", "next")
    def __init__(self, key="", value="", expiry=None):
        self.key, self.value, self.expiry = key, value, expiry
        self.prev = self.next = self

class LRUCache:
    def __init__(self, cap, clock=time.monotonic):
        self.cap, self.clock, self.map = cap, clock, {}
        self.head = Node()  # 哨兵：head.next 最近，head.prev 最久

    def _unlink(self, n): n.prev.next, n.next.prev = n.next, n.prev
    def _push_front(self, n):
        n.next, n.prev = self.head.next, self.head
        self.head.next.prev = n; self.head.next = n
    def _drop(self, n):               # 链表和哈希表一起删
        self._unlink(n); del self.map[n.key]

    def get(self, key):
        n = self.map.get(key)
        if n is None: return None
        if n.expiry is not None and self.clock() >= n.expiry:
            self._drop(n); return None   # 惰性过期
        self._unlink(n); self._push_front(n)
        return n.value

    def set(self, key, value, ttl=None):
        exp = None if ttl is None else self.clock() + ttl
        n = self.map.get(key)
        if n: n.value, n.expiry = value, exp; self._unlink(n)
        else:
            n = self.map[key] = Node(key, value, exp)
            if len(self.map) > self.cap: self._drop(self.head.prev)
        self._push_front(n)
```
