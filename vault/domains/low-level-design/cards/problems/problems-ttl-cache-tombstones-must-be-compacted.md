---
id: problems-ttl-cache-tombstones-must-be-compacted
node: problems.components.ttl-cache
type: qa
step: 3
tags: [grown]
---
## Q
缓存用小顶堆按截止时刻管理过期。一个 key 被覆写就要改期，可堆不能删中间元素——标准解法是什么？只做一半会毁掉什么？

## A
标准解法是**惰性删除加墓碑**（tombstone，`heapq` 文档里的配方）：旧条目不从堆里拿走，只标成已删除，弹出时跳过。

只做这一半是这道题最隐蔽的失败：**一个容量 1000 的缓存，被反复覆写的热 key 能在堆里留下几十万个死条目**。你对外承诺了内存有界，内部一个私有结构把承诺毁掉了，而且没有任何公开 API 会暴露它。

所以必须补上**压实**（compaction），并把堆长度暴露成可断言的只读属性：

```python
def discard(self, key):
    entry = self._entries.pop(key, None)
    if entry is None:
        return
    entry[2] = _REMOVED
    self._stale += 1
    if self._stale > 32 and self._stale * 2 > len(self._heap):
        self._heap = [e for e in self._heap if e[2] is not _REMOVED]
        heapq.heapify(self._heap)
        self._stale = 0
```

重建一次 O(n)，摊到制造这些墓碑的 n/2 次操作上是 O(1)。**不变量只有能被断言，才算数**。
