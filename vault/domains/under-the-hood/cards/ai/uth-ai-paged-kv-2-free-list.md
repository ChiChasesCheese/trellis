---
id: uth-ai-paged-kv-2-free-list
node: ai.paged-kv
type: qa
step: 2
---
## Q
**空闲块怎样 O(1) 分配与回收**｜vLLM · v0.32

显存被切成几万个块。请求来了要立刻拿到空闲块，结束了要立刻还回去，还要能把某个块从中间拿走。vLLM 用什么结构？

## A
**背景。** 最简单的办法是一个栈或队列装着所有空闲块，拿和还都是 O(1)。但 vLLM 还有前缀缓存：空闲块里的数据可能还有用，新请求命中它时，要把它从空闲队列的中间摘走。栈和队列做不到 O(1) 的中间删除。

**结构。** 双向链表（doubly linked list）：每个块自带 `prev_free_block` 和 `next_free_block`，头尾各放一个永远不会被取走的哨兵（sentinel）块，省掉空表和边界的特判。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="12" y="60" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="30" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">头</text>
<line x1="48" y1="70" x2="70" y2="70" stroke="currentColor" stroke-width="1"/>
<polygon points="70,70 63,73 63,67" fill="currentColor"/>
<line x1="70" y1="80" x2="48" y2="80" stroke="currentColor" stroke-width="1"/>
<polygon points="48,80 55,77 55,83" fill="currentColor"/>
<rect x="70" y="60" width="36" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="88" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<line x1="106" y1="70" x2="128" y2="70" stroke="currentColor" stroke-width="1"/>
<polygon points="128,70 121,73 121,67" fill="currentColor"/>
<line x1="128" y1="80" x2="106" y2="80" stroke="currentColor" stroke-width="1"/>
<polygon points="106,80 113,77 113,83" fill="currentColor"/>
<rect x="128" y="60" width="36" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="146" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<line x1="164" y1="70" x2="186" y2="70" stroke="currentColor" stroke-width="1"/>
<polygon points="186,70 179,73 179,67" fill="currentColor"/>
<line x1="186" y1="80" x2="164" y2="80" stroke="currentColor" stroke-width="1"/>
<polygon points="164,80 171,77 171,83" fill="currentColor"/>
<rect x="186" y="60" width="36" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="204" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<line x1="222" y1="70" x2="244" y2="70" stroke="currentColor" stroke-width="1"/>
<polygon points="244,70 237,73 237,67" fill="currentColor"/>
<line x1="244" y1="80" x2="222" y2="80" stroke="currentColor" stroke-width="1"/>
<polygon points="222,80 229,77 229,83" fill="currentColor"/>
<rect x="244" y="60" width="36" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="262" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<line x1="280" y1="70" x2="302" y2="70" stroke="currentColor" stroke-width="1"/>
<polygon points="302,70 295,73 295,67" fill="currentColor"/>
<line x1="302" y1="80" x2="280" y2="80" stroke="currentColor" stroke-width="1"/>
<polygon points="280,80 287,77 287,83" fill="currentColor"/>
<rect x="302" y="60" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="320" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">尾</text>
<text x="88" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先分出去</text>
<text x="262" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最晚被分出</text>
<line x1="204" y1="118" x2="204" y2="90" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="204,90 207,97 201,97" style="fill:var(--accent,#3b6fd4)"/>
<text x="204" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">命中: 把 5 号从中间摘走</text>
<text x="170" y="180" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">双向链表加头尾哨兵: 两端取放和中间摘除都是 O(1)</text>
</svg>
```

**细节。**

- 从头部取、往尾部放、知道块对象就能 O(1) 摘走中间的块
- 源码注释写明不用 Python 内置的 `deque`，因为它没法 O(1) 删中间；链表指针直接存在块对象上，不额外分配对象
- 队列初始按块号排，之后按「最久没用的在前」排

**为什么。** 块对象自己当链表节点，哪怕有几万个块，每次操作也只改几个指针。

**例题：** LC 146 LRU 缓存

设计容量固定的 LRU 缓存，`get` 和 `put` 都要 `O(1)`，满了就删最久没用的键。例：容量 2，`put(1,1)`、`put(2,2)`、`get(1)` → `1`，`put(3,3)` 淘汰键 `2`。双向链表加头尾哨兵，正是这里的空闲块队列。

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
