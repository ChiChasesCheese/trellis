---
id: uth-redis-eviction-expire-1-approx-lru
node: redis.eviction-expire
type: qa
step: 1
---
## Q
**Redis 的 LRU 为什么是“近似”的**｜Redis · 8.10

内存满了要淘汰最久没用的键，Redis 为什么不像 LeetCode 那样维护一条 LRU 链表？

## A
**背景。** 内存满了要淘汰“最久没被用过”的键。LeetCode 的做法：哈希表加双向链表，每次访问都把键挪到链表头。精确，但每个键要多存两个指针，每次读取都要改链表。Redis 的办法：别追求精确，随机抽几个，在其中挑最久没用的。

**结构。** 每个键只存一个 24 位的访问时间戳（精度 1 秒）；淘汰时随机采样，不维护全局顺序。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">不维护全局顺序: 随机抽 5 个, 淘汰空闲最久的</text>
<rect x="10" y="30" width="58" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="39" y="47" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空闲</text>
<text x="39" y="62" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">12 秒</text>
<rect x="74" y="30" width="58" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="103" y="47" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空闲</text>
<text x="103" y="62" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">340 秒</text>
<rect x="138" y="30" width="58" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="167" y="47" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空闲</text>
<text x="167" y="62" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">7 秒</text>
<rect x="202" y="30" width="58" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="231" y="47" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空闲</text>
<text x="231" y="62" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">95 秒</text>
<rect x="266" y="30" width="58" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="295" y="47" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空闲</text>
<text x="295" y="62" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2 秒</text>
<text x="8" y="94" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">每个键只存 24 位的访问时间戳 (精度 1 秒)</text>
<text x="8" y="112" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">抽到的键进 16 位置的候选池 (跨轮保留)</text>
<rect x="10" y="122" width="36" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="50" y="122" width="36" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="90" y="122" width="36" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="130" y="122" width="36" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="170" y="122" width="36" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="210" y="122" width="36" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="250" y="122" width="36" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="290" y="122" width="36" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="10" y="122" width="36" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="28" y="135.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">340</text>
<rect x="50" y="122" width="36" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="68" y="135.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">95</text>
<text x="8" y="164" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">精确 LRU 要给每个键多存链表指针,</text>
<text x="8" y="180" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每次读还要挪节点; 采样读时只写时间戳</text>
</svg>
```

**细节。**

- 每轮随机抽 `maxmemory-samples` 个键，默认 5 个，上限 64
- 抽到的键放进 16 个位置的候选池（跨轮保留），淘汰空闲最久的
- 24 位秒级时间戳约 194 天回绕一次

**为什么。** 精确 LRU 要给每个键多存链表指针，每次读取还要挪节点；采样只花 3 字节，读时只写一个时间戳。

**例题：** LC 146 LRU 缓存（同类：LC 460 LFU 缓存）

设计 `LRUCache(capacity)`：`get(key)` 命中返回值，否则 `-1`；`put(key, value)` 写入，超过容量就淘汰最久未使用的键；两个操作都要 O(1)。例：容量 2，`put(1,1)`、`put(2,2)`、`get(1)` → `1`、`put(3,3)` 淘汰键 `2`。这是精确版：哈希表加双向链表。

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0) -> None:
        self.key, self.val = key, val
        self.prev: Node | None = None
        self.next: Node | None = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.map: dict[int, Node] = {}
        self.head, self.tail = Node(), Node()      # 哨兵：head.next 是最近使用，tail.prev 是最久未使用
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node: Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node: Node) -> None:
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._unlink(node)                         # 摘下来再放到最前面 = 标记为刚用过
        self._push_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.cap:              # 满了：逐出链表尾部（最久未使用）
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]
        node = self.map[key] = Node(key, value)
        self._push_front(node)
```
