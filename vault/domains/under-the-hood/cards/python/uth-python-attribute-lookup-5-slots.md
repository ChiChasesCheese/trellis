---
id: uth-python-attribute-lookup-5-slots
node: python.attribute-lookup
type: qa
step: 5
---
## Q
**`__slots__` 省了什么**｜Python · CPython 3.14

给链表节点类加上 `__slots__ = ("key", "val", "prev", "next")`，实例为什么变小了，又为什么不能再随便加属性？

## A
**背景。** 普通实例要备好一个能随时增删属性的表。可节点这类对象成千上万个，属性是固定的，这份灵活性就是浪费。

**结构。** 声明 `__slots__` 之后，实例不再有 `__dict__`，对象里按声明的顺序留出固定的格子；类里为每个名字放一个成员描述符（`member_descriptor`），读写属性就是按偏移量取格子。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<text x="10" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4 个属性 每实例占用 CPython 3.14.8 实测</text>
<text x="10" y="48" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">普通实例 约 104 字节</text>
<rect x="10" y="56" width="260" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="10" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">__slots__ 64 字节</text>
<rect x="10" y="114" width="160" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="180" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">省约 40 字节</text>
<text x="170" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">64 = GC 头 16 + 对象头 16 + 4 格 x 8</text>
</svg>
```

**细节。**

- 实测（CPython 3.14.8，4 个属性，`tracemalloc`）：普通实例约 104 字节，`__slots__` 实例 64 字节。
- 3.11 起普通实例也在压缩属性的存储，所以省得比老版本少。
- 给没声明的名字赋值，报 `AttributeError: 'B' object has no attribute 'extra' and no __dict__ for setting new attributes`。
- 子类不写 `__slots__` 就重新拥有 `__dict__`；没有 `__weakref__` 槽的类也不能被弱引用。

**为什么。** 拿灵活性换内存：属性固定、实例数量大才划算。

**例题：** LC 146 LRU 缓存

设计 `LRUCache(capacity)`：`get(key)` 命中返回值否则返回 `-1`，`put(key, value)` 写入并在超出容量时淘汰最久未使用的键，两个操作都要 O(1)。

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
