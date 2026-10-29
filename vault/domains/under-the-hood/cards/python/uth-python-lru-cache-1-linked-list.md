---
id: uth-python-lru-cache-1-linked-list
node: python.lru-cache
type: qa
step: 1
---
## Q
**lru_cache 怎么 O(1) 淘汰最久没用的**｜Python · CPython 3.14

`@lru_cache(maxsize=2)` 命中时做什么？缓存满了怎么淘汰？

## A
**背景。** 函数算一次很贵时，把结果记下来，下次同样的参数直接取，这是缓存。内存有限，只留最近用过的 N 个，满了丢最久没用的（LRU，Least Recently Used）。最直接是用列表按使用顺序存，但每次查找、挪动都要 O(n)。

**结构。** 一个 `dict`（key 到链表节点）加一条带哨兵节点 `root` 的环形双向链表（C 实现）。例（`maxsize=2`）：调用 `f(1)`、`f(2)`、`f(1)`（命中，挪到最新）、`f(3)`（满了，丢最旧的 2）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="122" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最旧</text>
<text x="226" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最新</text>
<text x="14" y="46" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">f(1)</text>
<rect x="100" y="28" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="122" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="14" y="84" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">f(2)</text>
<rect x="100" y="66" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="122" y="83" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="152" y="66" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="174" y="83" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="14" y="122" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">f(1) 命中</text>
<rect x="100" y="104" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="122" y="121" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="152" y="104" width="44" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="174" y="121" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="326" y="122" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 挪到最新</text>
<text x="14" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">f(3) 满了</text>
<rect x="100" y="142" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="122" y="159" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="152" y="142" width="44" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="174" y="159" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="326" y="160" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">淘汰 2</text>
<text x="170" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">容量 2 每次命中或新增都放到最新一端</text>
</svg>
```

**细节。**

- 命中：查 `dict` 找到节点，摘下来接到链表尾，O(1)。
- 满了：取 `root.next`（最久没用的）出来，从 `dict` 删掉，**复用同一个节点**装新的 key 和结果，接到链表尾。
- 实测依次调用 `f(1) f(2) f(1) f(3) f(2)`：`hits=1, misses=4, currsize=2`。

**为什么。** `dict` 负责 O(1) 查找，链表负责 O(1) 调整顺序，复用节点省掉一次分配和释放。

**例题：** LC 146 LRU 缓存

设计 `LRUCache(capacity)`：`get(key)` 命中返回值，否则返回 `-1`；`put(key, value)` 写入，超出容量时淘汰最久未使用的键。两个操作都要 O(1)。例：容量 2，`put(1,1)`、`put(2,2)`、`get(1)` 得 `1`、`put(3,3)` 淘汰键 `2`、`get(2)` 得 `-1`。

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
