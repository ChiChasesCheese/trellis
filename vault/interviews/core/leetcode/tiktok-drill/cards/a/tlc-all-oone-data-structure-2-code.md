---
id: tlc-all-oone-data-structure-2-code
node: a.all-oone-data-structure
type: qa
step: 2
---
## Q
**LC 432 全 O(1) 的数据结构**｜写出 Python 实现

实现 `AllOne`：`inc(key)`、`dec(key)`（计数减到 `0` 就删除该 key）、`getMaxKey()`、`getMinKey()`（返回任意一个计数最大 / 最小的 key，空时返回 `""`）。`key` 由小写字母组成，长度 `1` 到 `10`，最多调用 `5 * 10^4` 次，五个操作都要求平均 `O(1)`。

## A
**思路。** 双向链表的每个节点是一个桶 `Bucket(cnt, keys)`，计数从小到大排列；字典 `where` 记 key 所在的桶。`inc` / `dec` 把 key 搬进相邻的桶（没有就新建），空桶立即摘掉。头尾用计数为 `0` 和 `-1` 的哨兵。

```python
class Bucket:
    __slots__ = ("cnt", "keys", "prev", "next")

    def __init__(self, cnt: int = 0) -> None:
        self.cnt = cnt
        self.keys: set[str] = set()
        self.prev: Bucket | None = None
        self.next: Bucket | None = None


class AllOne:
    def __init__(self) -> None:
        self.head, self.tail = Bucket(0), Bucket(-1)   # 哨兵：head.next 是最小计数桶，tail.prev 是最大
        self.head.next, self.tail.prev = self.tail, self.head
        self.where: dict[str, Bucket] = {}              # key -> 它当前所在的桶

    def _insert_after(self, node: Bucket, cnt: int) -> Bucket:
        new = Bucket(cnt)
        new.prev, new.next = node, node.next
        node.next.prev = new
        node.next = new
        return new

    def _remove(self, node: Bucket) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def inc(self, key: str) -> None:
        cur = self.where.get(key)
        anchor = self.head if cur is None else cur      # 新桶（计数 +1）该插在 anchor 后面
        target = anchor.next
        new_cnt = anchor.cnt + 1
        if target.cnt != new_cnt:                       # 相邻桶不是 cnt + 1 就新建一个
            target = self._insert_after(anchor, new_cnt)
        target.keys.add(key)
        self.where[key] = target
        if cur is not None:
            cur.keys.discard(key)
            if not cur.keys:
                self._remove(cur)                       # 空桶要摘掉，否则 getMinKey 会读到空集合

    def dec(self, key: str) -> None:
        cur = self.where[key]
        if cur.cnt == 1:
            del self.where[key]                         # 计数归零：key 彻底删除
        else:
            target = cur.prev
            if target.cnt != cur.cnt - 1:
                target = self._insert_after(cur.prev, cur.cnt - 1)
            target.keys.add(key)
            self.where[key] = target
        cur.keys.discard(key)
        if not cur.keys:
            self._remove(cur)

    def getMaxKey(self) -> str:
        if self.tail.prev is self.head:
            return ""
        return next(iter(self.tail.prev.keys))          # 任取一个即可

    def getMinKey(self) -> str:
        if self.head.next is self.tail:
            return ""
        return next(iter(self.head.next.keys))
```

运行：`inc("hello")` ×2 后 `getMaxKey()` → `"hello"`，`getMinKey()` → `"hello"`；`inc("leet")` 后 `getMaxKey()` → `"hello"`，`getMinKey()` → `"leet"`；空结构两者都是 `""`；`inc("a")`、`dec("a")` 后两者都是 `""`。

**复杂度。** 五个操作都是 `O(1)`；空间 `O(n)`。

**写法要点。**
- `__slots__` 去掉每个节点的 `__dict__`，桶很多时省内存、属性访问更快。
- `self.prev: Bucket | None` 写在 `__init__` 的函数体里，属性注解不会在运行时求值，所以类名可以直接出现；如果写在方法**签名**里（类还没定义完），Python 3.12 要加引号 `"Bucket"` 或 `from __future__ import annotations`，否则 `NameError`。
- `next(iter(some_set))` 取集合里任意一个元素，`O(1)`，不删除；`set.pop()` 会删除，这里不能用。
- `inc` 的顺序：先把 key 放进目标桶（必要时新建），再检查并摘除原桶；顺序反了新桶会插到被摘掉的节点后面。
- `dec` 的 `cur.cnt == 1` 分支不挪桶，只从 `where` 删除。
