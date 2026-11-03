---
id: craft-lazy-deletion-heap-3-compaction
node: craft.patterns.lazy-deletion-heap
type: qa
step: 3
---
## Q
**惰性删除堆 · 墓碑堆积和压实**｜模式

TTL 缓存承诺最多 1000 条。有人对同一个 key 反复覆写十万次，每次覆写都在到期堆里留下一个旧条目。不做任何处理，堆会变成多大？怎么治，成本是多少？

## A
**要点。** 堆会涨到十万个条目，而缓存里只有一个 key：「只有 1000 条」的承诺在堆上被悄悄打破。治法是压实（compaction）：墓碑数超过堆的一半时，一次性过滤掉墓碑并重建堆。

```python
def set(self, key, exp):
    old = self.entry.pop(key, None)
    if old is not None:
        old[2] = REMOVED                       # 墓碑：只标记
        self.stale += 1
    e = [exp, key, key]; self.entry[key] = e
    heapq.heappush(self.heap, e)
    if self.stale > len(self.heap) // 2:       # 墓碑超过一半
        self._compact()

def _compact(self):
    self.heap = [e for e in self.heap if e[2] is not REMOVED]
    heapq.heapify(self.heap)                   # O(n)
    self.stale = 0
```

同一个 key 覆写十万次：

```
不压实 -> 缓存里 1 个 key，堆里有 100000 个条目
压实 -> 缓存里 1 个 key，堆里有 2 个条目
```

**为什么摊还 O(1)。** 压实是 O(n)，但要先积累 n/2 个墓碑才触发，每个墓碑平均只分担常数的重建成本。

**易错。** 触发条件要看墓碑数，而不是堆的大小：任务调度器按取消次数压实，连续取消一百万个未到期任务，堆也不会涨到一百万。
