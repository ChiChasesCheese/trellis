---
id: uth-ai-prefix-cache-3-eviction
node: ai.prefix-cache
type: qa
step: 3
---
## Q
**缓存满了先淘汰谁**｜vLLM · SGLang

显存有限，缓存的前缀越攒越多。两个系统各按什么顺序淘汰，怎样保证正在用的块不被淘汰？

## A
**背景。** 缓存满了就得丢一部分，通用做法是最近最少使用（LRU）。难点有两个：正在被请求使用的块不能丢；前缀的中间块不能比尾部块先丢，否则后面的块即使还在，也再没人能命中。

**结构。**

- vLLM：每个块有引用计数 `ref_cnt`。降到 0 的块不立刻丢，放回空闲队列末尾，哈希还在，仍可命中；分配新块从队首取，这时才抹掉哈希。命中时 `ref_cnt` 加 1，并从队列中间摘走
- SGLang：只淘汰叶子，可淘汰的叶子放进最小堆，按最后访问时间弹出最老的；父节点没有孩子了，也入堆

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<text x="12" y="18" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个请求结束, 它的块倒着放回空闲队列</text>
<rect x="20" y="50" width="56" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="48" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">块3</text>
<line x1="76" y1="65" x2="94" y2="65" stroke="currentColor" stroke-width="1"/>
<polygon points="94,65 87,68 87,62" fill="currentColor"/>
<rect x="94" y="50" width="56" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="122" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">块2</text>
<line x1="150" y1="65" x2="168" y2="65" stroke="currentColor" stroke-width="1"/>
<polygon points="168,65 161,68 161,62" fill="currentColor"/>
<rect x="168" y="50" width="56" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="196" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">块1</text>
<line x1="224" y1="65" x2="242" y2="65" stroke="currentColor" stroke-width="1"/>
<polygon points="242,65 235,68 235,62" fill="currentColor"/>
<rect x="242" y="50" width="56" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="270" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">块0</text>
<text x="48" y="40" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">最先被淘汰</text>
<text x="270" y="40" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最后</text>
<text x="170" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">尾部的块只对更长的前缀有用, 先淘汰</text>
<text x="170" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">开头的块人人都用, 留到最后</text>
<text x="170" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">块被别的请求命中时, 从队列中摘走</text>
</svg>
```

**细节。**

- vLLM 释放一个请求的块时倒着放回，同一个请求的尾块在队列里比头块靠前，先被淘汰

**为什么。** 尾部的块只对更长的前缀有用，开头的块谁都要用；先丢尾巴，缓存里留下的永远是还能命中的完整前缀。

**例题：** LC 146 LRU 缓存

设计容量固定的 LRU 缓存，`get` 和 `put` 都要 `O(1)`，满了就删最久没用的键。例：容量 2，`put(1,1)`、`put(2,2)`、`get(1)` → `1`，`put(3,3)` 淘汰键 `2`。

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
