---
id: tlc-patterns-design-6-allone
node: patterns.design
type: qa
step: 6
---
## Q
**数据结构设计题｜全 O(1) 的数据结构（LC 432）：按计数分桶的双向链表**

`inc`、`dec`、`getMaxKey`、`getMinKey` 都要平均 `O(1)`。为什么堆不行，桶链怎么设计？

## A
堆的更新是 `O(log n)`。改用**按计数分桶**：每个桶存"计数相同的所有 key"，桶按计数从小到大排成**双向链表**。`inc`/`dec` 只会把 key 挪到**相邻**的桶，最大 / 最小就是链表两端的桶。

```python
class Bucket:
    def __init__(self, count: int) -> None:
        self.count = count
        self.keys: set[str] = set()
        self.prev: "Bucket | None" = None
        self.next: "Bucket | None" = None

class AllOne:
    def __init__(self) -> None:
        self.head, self.tail = Bucket(0), Bucket(0)   # 哑头（最小侧）、哑尾（最大侧）
        self.head.next, self.tail.prev = self.tail, self.head
        self.where: dict[str, Bucket] = {}            # key -> 所在的计数桶

    def _insert_after(self, node: Bucket, count: int) -> Bucket:
        b = Bucket(count)
        b.prev, b.next = node, node.next
        node.next.prev = b
        node.next = b
        return b

    def _remove_if_empty(self, b: Bucket) -> None:
        if not b.keys:
            b.prev.next, b.next.prev = b.next, b.prev

    def inc(self, key: str) -> None:
        cur = self.where.get(key)
        base = self.head if cur is None else cur
        nxt = base.next
        if nxt is self.tail or nxt.count != base.count + 1:
            nxt = self._insert_after(base, base.count + 1)   # 没有计数 +1 的桶就新建
        nxt.keys.add(key)
        self.where[key] = nxt
        if cur is not None:
            cur.keys.remove(key)
            self._remove_if_empty(cur)

    def dec(self, key: str) -> None:
        cur = self.where[key]
        if cur.count == 1:
            del self.where[key]
        else:
            prv = cur.prev
            if prv is self.head or prv.count != cur.count - 1:
                prv = self._insert_after(cur.prev, cur.count - 1)
            prv.keys.add(key)
            self.where[key] = prv
        cur.keys.remove(key)
        self._remove_if_empty(cur)

    def getMaxKey(self) -> str:
        return next(iter(self.tail.prev.keys)) if self.tail.prev is not self.head else ""

    def getMinKey(self) -> str:
        return next(iter(self.head.next.keys)) if self.head.next is not self.tail else ""

a = AllOne(); a.inc("hello"); a.inc("hello")
print(a.getMaxKey(), a.getMinKey())   # hello hello
a.inc("leet")
print(a.getMaxKey(), a.getMinKey())   # hello leet
```

- `inc` 与 `dec` 统一成"找到相邻桶，没有就新建"；新 key 的"当前桶"视为哑头（计数 0）。
- 桶空了必须摘链（`_remove_if_empty`），否则 `getMinKey` 可能取到空桶。
