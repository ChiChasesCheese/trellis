---
id: tlc-lfu-cache-5-alt
node: a.lfu-cache
type: qa
step: 5
---
## Q
**LC 460 LFU 缓存**｜另一种解法

如果放宽到 `O(log n)`，有没有更短、更不容易写错的写法？它怎么维护淘汰顺序，代价是什么，什么时候该选它？

## A
**思路：堆 + 惰性删除。** 每个键保存 `[值, 次数, 最近使用的时间戳]`；堆里放 `(次数, 时间戳, 键)`。每次使用一个键，就更新它的次数和时间戳，并把新条目压入堆；旧条目不去堆里找、不删除，等它被弹出时再判断："这条记录的次数和时间戳是否仍与该键当前的值相同"，不相同就是过期条目，丢掉继续弹。时间戳用递增的逻辑时钟，自然实现"次数相同则最久未使用先淘汰"。

```python
import heapq

class LFUCacheHeap:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.tick = 0                                        # 逻辑时钟，决定「最久未使用」
        self.data: dict[int, list[int]] = {}                 # key -> [value, 次数, 最近一次使用的时间]
        self.heap: list[tuple[int, int, int]] = []           # (次数, 时间, key)，可能含过期条目

    def _use(self, key: int) -> None:
        self.tick += 1
        entry = self.data[key]
        entry[1] += 1
        entry[2] = self.tick
        heapq.heappush(self.heap, (entry[1], entry[2], key))  # 旧条目不删，弹出时再识别

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self._use(key)
        return self.data[key][0]

    def put(self, key: int, value: int) -> None:
        if key in self.data:
            self.data[key][0] = value
            self._use(key)
            return
        if len(self.data) >= self.capacity:
            while True:                                      # 跳过过期条目，直到遇到当前有效的那条
                freq, stamp, victim = heapq.heappop(self.heap)
                entry = self.data.get(victim)
                if entry is not None and entry[1] == freq and entry[2] == stamp:
                    del self.data[victim]
                    break
        self.tick += 1
        self.data[key] = [value, 1, self.tick]
        heapq.heappush(self.heap, (1, self.tick, key))
```

运行：题面的操作序列返回值与桶版本相同：`1, -1, 3, -1, 3, 4`；`10^5` 次 `put` 加 `10^5` 次 `get` 约 `0.06` 秒。

**复杂度。** 每次操作 `O(log n)`（摊销）；空间：堆里会堆积过期条目，只有淘汰时才会清理，最坏随操作次数增长 `O(调用次数)`，不再是 `O(capacity)`。

**什么时候选哪个。**
- 桶 + `OrderedDict`（主解法）：严格 `O(1)`、空间 `O(capacity)`，符合题目要求，面试里默认写这个。
- 堆 + 惰性删除：代码短、概念简单（"最小的 `(次数, 时间)`"），不需要维护 `min_freq` 这类容易漏更新的变量；适合放宽到 `O(log n)` 的场景，或者先给出一个正确的版本再优化。代价是堆可能因为过期条目膨胀，需要定期重建。

**Python 提醒**：元组比较是逐元素的，`(次数, 时间, 键)` 先比次数再比时间，时间戳互不相同，所以不会比到键；如果时间戳可能重复，键之间要能比较大小，否则会抛 `TypeError`。
