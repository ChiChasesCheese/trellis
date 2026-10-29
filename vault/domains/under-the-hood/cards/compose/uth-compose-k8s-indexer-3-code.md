---
id: uth-compose-k8s-indexer-3-code
node: compose.k8s-indexer
type: qa
step: 3
---
## Q
**不变量与核心代码**｜Kubernetes · client-go v0.37

主表和所有索引之间必须保持什么关系？写入时按什么顺序更新？

## A
**不变量。** 对象 o（key 为 k）在 `items` 里，当且仅当：对每个索引、索引函数给 o 算出的每个值 v，k 都在 `indices[名][v]` 里；反过来，索引里出现的 key 一定在 `items` 里。

**细节。**

- 改对象时必须同时拿到**旧对象**和新对象：用旧对象算出旧分组，把 k 摘掉；用新对象算出新分组，把 k 挂上
- 顺序：先从 `items` 取出旧对象，写入新对象，再更新索引；删除则先更新索引，再删 `items`
- 分组里的集合变空，要把这个分组也删掉，否则"一次性对象"多的索引会攒下越来越多空集合

```python
from typing import Any, Callable

IndexFunc = Callable[[Any], list[str]]


class Indexer:
    def __init__(self, funcs: dict[str, IndexFunc]) -> None:
        self.items: dict[str, Any] = {}      # 主表：key -> 对象
        self.funcs = funcs                   # 索引名 -> 从对象算出它属于哪些分组
        self.indices: dict[str, dict[str, set[str]]] = {n: {} for n in funcs}   # 索引名 -> 分组值 -> key 集合

    def upsert(self, key: str, obj: Any) -> None:
        old = self.items.get(key)
        self.items[key] = obj
        self._reindex(key, old, obj)

    def delete(self, key: str) -> None:
        if key in self.items:
            self._reindex(key, self.items.pop(key), None)

    def by_index(self, name: str, value: str) -> list[Any]:
        return [self.items[k] for k in self.indices[name].get(value, ())]

    def _reindex(self, key: str, old: Any, new: Any) -> None:
        for name, fn in self.funcs.items():
            index = self.indices[name]
            for v in set(fn(old)) if old is not None else ():   # 先按旧对象，把 key 从旧分组摘掉
                index[v].discard(key)
                if not index[v]:
                    del index[v]             # 分组空了就删，免得空集合越攒越多
            for v in set(fn(new)) if new is not None else ():   # 再按新对象，把 key 挂到新分组
                index.setdefault(v, set()).add(key)
```

**例题：** LC 432 全 O(1) 的数据结构（同类：LC 460 LFU 缓存）

实现 `AllOne`：`inc(key)` 让计数加 1，不存在则插入计数为 1 的 key；`dec(key)` 让计数减 1，减到 0 就删除；`getMaxKey()` / `getMinKey()` 返回计数最大 / 最小的 key（没有则返回 `""`）。每个操作平均 O(1)。例：`inc("hello")` 两次、`inc("leet")` 一次后，`getMaxKey()` 得 `"hello"`，`getMinKey()` 得 `"leet"`。

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
