---
id: uth-os-net-rate-limit-3-state
node: os-net.rate-limit
type: qa
step: 3
---
## Q
**限流的每个 IP 状态放哪里**｜Nginx · limit_req_zone · 1.31

给每个客户端记一份限流状态，几十万个 IP 怎么不撑爆内存？

## A
**背景。** 限流要为每个客户端各记一份状态（`excess` 和上次到达的时间）。几十万个 IP 时，状态放哪里、怎样快速查到、满了怎么办？Nginx 在共享内存区里放一棵红黑树（保持平衡的有序树，按 key 查找 O(log n)）加一条 LRU 队列（最近用过的挪到队头，满了就从队尾淘汰）。

**结构。** 红黑树负责“按 IP 找到状态”，LRU 队列负责“谁最久没用”。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<line x1="170" y1="50" x2="110" y2="58" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="170" y1="50" x2="230" y2="58" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="110" y1="86" x2="80" y2="94" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="110" y1="86" x2="140" y2="94" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="230" y1="86" x2="200" y2="94" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="230" y1="86" x2="260" y2="94" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="170" cy="36" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ip5</text>
<circle cx="110" cy="72" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ip2</text>
<circle cx="230" cy="72" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ip8</text>
<circle cx="80" cy="108" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ip1</text>
<circle cx="140" cy="108" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ip3</text>
<circle cx="200" cy="108" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="200" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ip7</text>
<circle cx="260" cy="108" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ip9</text>
<text x="14" y="20" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">红黑树 按 key 查找</text>
<text x="14" y="144" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">LRU 队列 最近访问的挪到队头</text>
<rect x="40" y="152" width="50" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="65" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ip8</text>
<line x1="90" y1="164" x2="105" y2="164" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M110.0,164.0 L103.2,167.3 L103.2,160.7 Z" fill="currentColor" stroke="none"/>
<rect x="110" y="152" width="50" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="135" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ip3</text>
<line x1="160" y1="164" x2="175" y2="164" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M180.0,164.0 L173.2,167.3 L173.2,160.7 Z" fill="currentColor" stroke="none"/>
<rect x="180" y="152" width="50" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ip5</text>
<line x1="230" y1="164" x2="245" y2="164" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M250.0,164.0 L243.2,167.3 L243.2,160.7 Z" fill="currentColor" stroke="none"/>
<rect x="250" y="152" width="50" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="275" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ip1</text>
<line x1="275" y1="176" x2="275" y2="187" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M275.0,192.0 L271.7,185.2 L278.3,185.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="283" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">满了淘汰</text>
</svg>
```

**细节。**

- 每条状态占 64 字节（32 位平台）或 128 字节（64 位平台）；1 MB 的区能存约 8000 条 128 字节的状态
- 区满了，从队尾淘汰最久没访问的状态
- key 用 `$binary_remote_addr`（IPv4 只要 4 字节，IPv6 16 字节），比文本形式的 `$remote_addr` 省空间

**为什么。** 红黑树 O(log n) 查找，LRU 链表 O(1) 淘汰：就是 LRU 缓存的“哈希表加双向链表”，只是哈希表换成了红黑树。

**例题：** LC 146 LRU 缓存（同类：LC 460 LFU 缓存）

设计 LRU 缓存 `LRUCache(capacity)`：`get(key)` 命中返回值，否则返回 -1；`put(key, value)` 写入，超出容量时淘汰最久未使用的键。`get`、`put` 都要平均 O(1)。

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
