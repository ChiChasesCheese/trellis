---
id: tlc-tt-lru-cache-ttl-5-alt
node: a.tt-lru-cache-ttl
type: qa
step: 5
---
## Q
**带 TTL 的 LRU 缓存**｜另一种解法

面试官要求手写「哈希表 + 双向链表」，不用 `OrderedDict`，也不想维护堆。带 TTL 的 LRU 缓存（满了先清过期再淘汰最久未用）怎样写？代价是什么，什么时候选它？

## A
**手写双向链表加整表扫描清过期。** 哨兵 `head`、`tail` 之间按使用顺序排，`head.next` 最久未用；满了就从头扫一遍链表，删掉所有过期节点，仍满再删 `head.next`。

```python
import time
from collections.abc import Callable


class _Node:
    def __init__(self, key: int = 0, value: int = 0, expire_at: float = 0.0) -> None:
        self.key, self.value, self.expire_at = key, value, expire_at
        self.prev: _Node | None = None
        self.next: _Node | None = None


class LRUCacheTTLList:
    def __init__(self, capacity: int, clock: Callable[[], float] = time.monotonic) -> None:
        self.cap, self.clock = capacity, clock
        self.map: dict[int, _Node] = {}
        self.head, self.tail = _Node(), _Node()          # 哨兵：head.next 最久未用，tail.prev 最近使用
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node: _Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_back(self, node: _Node) -> None:
        last = self.tail.prev
        last.next, node.prev, node.next, self.tail.prev = node, last, self.tail, node

    def _remove(self, node: _Node) -> None:
        self._unlink(node)
        del self.map[node.key]

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        if self.clock() >= node.expire_at:
            self._remove(node)
            return -1
        self._unlink(node)
        self._push_back(node)
        return node.value

    def put(self, key: int, value: int, ttl: float) -> None:
        now = self.clock()
        if node := self.map.get(key):                    # 已存在：覆盖、重置 TTL、变成最近使用
            node.value, node.expire_at = value, now + ttl
            self._unlink(node)
            self._push_back(node)
            return
        if len(self.map) >= self.cap:
            node = self.head.next
            while node is not self.tail:                 # 满了：整表扫一遍清过期，O(n)
                nxt = node.next
                if node.expire_at <= now:
                    self._remove(node)
                node = nxt
            if len(self.map) >= self.cap:
                self._remove(self.head.next)             # 仍满：淘汰最久未使用
        node = _Node(key, value, now + ttl)
        self.map[key] = node
        self._push_back(node)
```

`get` 为 `O(1)`；`put` 在缓存已满且新 key 时为 `O(n)`。

**怎么选。**
- 容量几百到几千、写入不频繁：这版够用，没有版本号和重建堆的细节，不容易写错，面试里 15 分钟能写完。
- 容量大、写入频繁：每次满都整表扫描撑不住，用 `OrderedDict` 加堆的版本，`put` 均摊 `O(log n)`。
- 先写这一版并说明瓶颈在「找全部过期条目」，再引出最小堆加版本号，是自然的升级路线。
