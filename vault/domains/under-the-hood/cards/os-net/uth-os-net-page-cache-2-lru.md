---
id: uth-os-net-page-cache-2-lru
node: os-net.page-cache
type: qa
step: 2
---
## Q
**页缓存的淘汰：两条 LRU 链表**｜Linux · 经典 LRU 与 MGLRU · 内核 6.12

页缓存满了该丢哪页？只读一遍的大文件为什么冲不掉热数据？

## A
**背景。** 内存有限，页缓存满了要丢页。最朴素的是 LRU（最近最少使用）：丢最久没碰过的页。可是顺序读一个超大文件，会把这些只用一次的页全部塞进来，把真正的热页挤出去。Linux 的办法：新页先放进“不活跃”链表，被再次访问才升级进“活跃”链表，也就是访问两次才算热。

**结构。** 文件页挂在不活跃和活跃两条链表上（`LRU_INACTIVE_FILE` 与 `LRU_ACTIVE_FILE`），回收优先从不活跃链表的尾部下手。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="70" y="34" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">不活跃链表</text>
<text x="70" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">活跃链表</text>
<rect x="70" y="40" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="70" y="118" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="114" y="40" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="114" y="118" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="158" y="40" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="158" y="118" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="202" y="40" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="202" y="118" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="30" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">新页</text>
<line x1="44" y1="54" x2="63" y2="54" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M68.0,54.0 L61.2,57.3 L61.2,50.7 Z" fill="currentColor" stroke="none"/>
<line x1="246" y1="54" x2="285" y2="54" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M290.0,54.0 L283.2,57.3 L283.2,50.7 Z" fill="currentColor" stroke="none"/>
<text x="312" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">淘汰</text>
<line x1="136" y1="66" x2="136" y2="113" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M136.0,118.0 L132.7,111.2 L139.3,111.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="146" y="96" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">再访问一次</text>
<text x="92" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">头</text>
<text x="224" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">尾</text>
</svg>
```

**细节。**

- 新页先进不活跃链表，被第二次访问才升入活跃链表
- 只读一遍的流式数据没有机会升级，直接从不活跃端淘汰
- 6.1 起有多代 LRU（MGLRU，`CONFIG_LRU_GEN`）：页按年龄分到最多 4 代（`MAX_NR_GENS`）

**为什么。** 单条 LRU 会被一次大文件扫描冲掉所有热页；“访问两次才算热”是便宜的抗扫描办法。

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
