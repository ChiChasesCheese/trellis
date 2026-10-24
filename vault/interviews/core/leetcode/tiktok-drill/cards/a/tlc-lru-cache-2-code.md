---
id: tlc-lru-cache-2-code
node: a.lru-cache
type: qa
step: 2
---
## Q
**LC 146 LRU 缓存**｜写出 Python 实现

实现 `LRUCache(capacity)`，`get(key)` 命中返回值、未命中返回 `-1`，`put(key, value)` 更新或插入，超出容量时逐出最久未使用的键；`get`、`put` 平均 `O(1)`。`1 <= capacity <= 3000`，`0 <= key <= 10000`，`0 <= value <= 10^5`，最多 `2 * 10^5` 次调用。要求手写双向链表加字典。

## A
**思路。** 字典存「键 → 节点」，双向链表从头到尾按「最近使用 → 最久未使用」排列，头尾用哨兵节点。访问或更新就把节点摘下放到链表头；插入新键前如果已满，先删链表尾部节点并用它的 `key` 删字典项。

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

运行：题面的操作序列输出 `[None, None, 1, None, -1, None, -1, 3, 4]`；容量 1：`put(1,1)`、`put(2,2)` 后 `get(1)` 得 `-1`、`get(2)` 得 `2`；容量 2：`put(1,1)`、`put(2,2)`、`put(1,10)`、`put(3,3)` 后 `get(1)` 得 `10`、`get(2)` 得 `-1`、`get(3)` 得 `3`。

**复杂度。** 每次操作 `O(1)`：一次字典操作加常数次指针修改；空间 `O(capacity)`。

**写法要点。** `__slots__` 去掉每个节点的 `__dict__`，节点多时省内存也更快；哨兵让 `_unlink` 和 `_push_front` 不用判断空链表；`_unlink` / `_push_front` 抽成小函数，`get` 和 `put` 的更新分支复用；`a.x, b.y = b.y, a.x` 先整体求值右边再赋值，摘节点的两步不会互相覆盖；`node = self.map[key] = Node(...)` 链式赋值一行完成创建和登记。
