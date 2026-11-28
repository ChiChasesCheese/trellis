---
id: mlp-coding-pc08-solve
node: coding.pc08
step: 1
type: qa
---
## Q
**带过期时间的 LRU 缓存与数据流中位数：题与解**｜编程轮

两道经典设计题放在一起。一，LRU 缓存（最近最少使用淘汰）：容量固定，`get` 命中返回值、未命中返回 -1，`put` 写入，超出容量时淘汰最久没用过的；`get` 和 `put` 都要 O(1)；再加上每个条目可选的过期时间 `ttl`。二，数据流中位数：不断 `add` 数字，随时能返回到目前为止的中位数。

## A
**一句话思路。** LRU 靠一个记住使用顺序的哈希表（`OrderedDict`，每次使用就移到末尾，淘汰就弹出开头）；过期是惰性的，到 `get` 时才检查截止时间。中位数用两个堆：大顶堆存较小的一半，小顶堆存较大的一半，两堆大小差不超过 1，中位数就在堆顶。

```python
import heapq, time
from collections import OrderedDict

class LRUCacheTTL:
    def __init__(self, capacity, clock=time.monotonic):   # 时钟可注入，测试里用假时钟
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity, self.clock = capacity, clock
        self.data = OrderedDict()      # 开头是最久未用，末尾是最近使用
        self.expiry = {}               # key -> 绝对截止时间；没有这一项表示永不过期

    def get(self, key):
        if key not in self.data:
            return -1
        deadline = self.expiry.get(key)
        if deadline is not None and self.clock() >= deadline:
            del self.data[key]         # 惰性清理：被读到时才发现过期，顺手删掉
            del self.expiry[key]
            return -1
        self.data.move_to_end(key)     # 标记为最近使用；get 不会延后过期时间
        return self.data[key]

    def put(self, key, value, ttl=None):
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if ttl is None:
            self.expiry.pop(key, None)
        else:
            self.expiry[key] = self.clock() + ttl   # 从写入时刻算起的绝对截止时间
        if len(self.data) > self.capacity:
            old, _ = self.data.popitem(last=False)  # 容量淘汰，与有没有 ttl 无关
            self.expiry.pop(old, None)

class MedianStream:
    def __init__(self):
        self.lo = []    # 大顶堆（存负数）：较小的一半
        self.hi = []    # 小顶堆：较大的一半

    def add(self, num):
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))   # 先过一遍，保证 lo 的最大值 <= hi 的最小值
        if len(self.hi) > len(self.lo):                    # 再平衡：lo 最多比 hi 多 1
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def median(self):
        if not self.lo:
            raise ValueError("empty stream")
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2

t = [0]
c = LRUCacheTTL(2, clock=lambda: t[0])
c.put(1, 100, ttl=5)
c.put(2, 200)
print(c.get(1))            # 100
t[0] = 6
print(c.get(1), c.get(2))  # -1 200
m = MedianStream()
for x in (5, 1, 3):
    m.add(x)
print(m.median())          # 3.0
m.add(4)
print(m.median())          # 3.5
```

**复杂度。** LRU 的 `get`、`put` 都是 O(1)；中位数 `add` 是 O(log n)，`median` 是 O(1)。

**边写边讲。**
- "`OrderedDict` gives O(1) **move-to-end and pop-oldest**; I can also hand-roll a doubly linked list plus a dict."
- "TTL is an **absolute deadline** checked lazily on `get`, and `get` doesn't extend it."
- "Two heaps turn each query into **O(1)**: the median sits at the top of the heaps."
