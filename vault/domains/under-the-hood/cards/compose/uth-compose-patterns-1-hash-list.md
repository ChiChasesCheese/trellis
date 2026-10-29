---
id: uth-compose-patterns-1-hash-list
node: compose.patterns
type: qa
step: 1
---
## Q
**哈希表 + 双向链表：O(1) 找到，O(1) 排序**｜LinkedHashMap · OpenJDK 25

缓存既要按 key 在 O(1) 内查到值，又要在 O(1) 内挑出“最久没用”的那个淘汰。一种结构做不到，该怎么拼？

## A
**背景。** 哈希表（hash table）按 key 查是 O(1)，但不记顺序，找“最久没用的”要整张扫；链表能记顺序，但找某个节点要从头走。哈希表负责找到，链表负责排序。

**结构。** 哈希表的 value 直接存链表节点；链表按使用时间排，表头最久没用。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="14" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">哈希表: key 直接指向节点</text>
<rect x="40" y="28" width="56" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="68.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">key b</text>
<line x1="68" y1="54" x2="68" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="68.0,100.0 65.5,95.0 70.5,95.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="130" y="28" width="56" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="158.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">key c</text>
<line x1="158" y1="54" x2="158" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="158.0,100.0 155.5,95.0 160.5,95.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="220" y="28" width="56" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="248.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">key a</text>
<line x1="248" y1="54" x2="248" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="248.0,100.0 245.5,95.0 250.5,95.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="40" y="102" width="56" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="68.0" y="120.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="130" y="102" width="56" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="158.0" y="120.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="220" y="102" width="56" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="248.0" y="120.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="96" y1="116" x2="130" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="130.0,116.0 125.0,118.5 125.0,113.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="96.0,116.0 101.0,113.5 101.0,118.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="186" y1="116" x2="220" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="220.0,116.0 215.0,118.5 215.0,113.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="186.0,116.0 191.0,113.5 191.0,118.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="68" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最久没用</text>
<text x="248" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最近用过</text>
<text x="170" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">双向链表 = 使用顺序  头尾都能 O(1) 增删</text>
</svg>
```

| 操作 | 做法 | 复杂度 |
|---|---|---|
| 查 key | 哈希表给出节点 | O(1) |
| 标记刚用过 | 摘下节点，接到表尾 | O(1) |
| 淘汰 | 取表头，用节点里的 key 删哈希表项 | O(1) |

**细节。**

- Java `LinkedHashMap`：节点多 `before`、`after`；`accessOrder=true` 时每次访问移到表尾，插入后调用 `removeEldestEntry(表头)`
- Python `OrderedDict`（CPython 3.13 的 C 实现）：另存一个与字典槽位对齐的节点数组，否则找节点要 O(n)

**为什么。** 链表必须双向：摘中间节点要改前驱的指针。节点里必须存 key：淘汰时手里只有节点，要靠它回头删哈希表项。

**坑。** 只摘了链表、忘了删哈希表，表里就留下悬空引用。

**例题：** LC 146 LRU 缓存（同类：LC 460 LFU 缓存、LC 432 全 O(1) 的数据结构）

设计 `LRUCache(capacity)`：`get(key)` 命中返回值，否则返回 `-1`；`put(key, value)` 写入，超出容量时淘汰最久未使用的键。两个操作都要平均 `O(1)`。例：容量 2，`put(1,1)`、`put(2,2)`、`get(1)` 得 `1`、`put(3,3)` 淘汰键 `2`、`get(2)` 得 `-1`。

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
