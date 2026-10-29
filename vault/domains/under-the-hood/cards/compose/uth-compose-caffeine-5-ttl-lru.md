---
id: uth-compose-caffeine-5-ttl-lru
node: compose.caffeine
type: qa
step: 5
---
## Q
**借到面试题：带 TTL 的 LRU 缓存**｜Caffeine · 3.3.1

面试要你手写固定容量、每条自带 TTL（存活时间）、`get` 与 `put` 均摊 O(1) 的缓存。怎样用同一个骨架拼出来？

## A
**结构。** 哈希表 + 双向链表（Python 里一个 `OrderedDict`）管查值和「淘汰最久未用」；再加一个按到期时刻排序的最小堆，专门回答「哪些条目已经过期」，它在 Caffeine 里对应「每条自定到期时间」时用的时间轮（一圈格子，每格挂一批同一时段到期的条目）。

**细节。**

- 读到过期条目当场删掉；写入时容量满了，先弹堆顶清掉所有过期条目，仍满再淘汰链表头。
- 堆不能快速删掉中间的元素，覆盖写之后堆里会留着旧条目：每次写入给一个递增版本号，弹出时和当前版本对不上就丢掉。

**为什么。** 链表按「使用顺序」排，没法回答「谁先到期」；两种顺序各配一个结构，再让哈希表指向同一份数据。Caffeine 里逐条自定到期时间的过期是 O(1)，靠时间轮代替了这里的堆；存活时间固定时，一条按写入顺序的队列就够，不需要堆。

**坑。** 堆项不带版本号，会把被覆盖写过的活条目当作过期误删。

**例题：** 带 TTL 的 LRU 缓存

固定容量 `capacity` 的 LRU 缓存，`get(key)` 命中返回值否则 -1，`put(key, value, ttl)` 带每条自己的存活秒数。过期条目读到时当作不存在；满了先清过期条目，仍满再淘汰最久未使用的；两个操作均摊 O(1)。例：容量 2，`put(1,1,ttl=5)`、`put(2,2,ttl=10)`，`get(1)` → 1；`put(3,3,ttl=10)` 淘汰键 2；6 秒后 `get(1)` → -1。

```python
import heapq
import time
from collections import OrderedDict
from collections.abc import Callable


class LRUCacheTTL:
    def __init__(self, capacity: int, clock: Callable[[], float] = time.monotonic) -> None:
        self.cap = capacity
        self.clock = clock                                  # 可注入的时钟，测试时换成假时钟
        self.data: OrderedDict[int, tuple[int, float]] = OrderedDict()   # key -> (value, 到期时刻)，队尾最近使用
        self.expiry: list[tuple[float, int, int]] = []      # 最小堆：(到期时刻, 写入版本, key)
        self.version: dict[int, int] = {}                   # key -> 当前有效的写入版本
        self.counter = 0

    def get(self, key: int) -> int:
        item = self.data.get(key)
        if item is None:
            return -1
        value, expire_at = item
        if self.clock() >= expire_at:      # 读到过期条目：懒删除，当作不存在
            self._drop(key)
            return -1
        self.data.move_to_end(key)         # 命中：变成最近使用（不刷新 TTL）
        return value

    def put(self, key: int, value: int, ttl: float) -> None:
        now = self.clock()
        if key not in self.data and len(self.data) >= self.cap:
            self._purge_expired(now)       # 先清过期条目
            if len(self.data) >= self.cap:
                oldest = next(iter(self.data))
                self._drop(oldest)         # 仍满：淘汰最久未使用
        self.counter += 1
        self.data[key] = (value, now + ttl)
        self.data.move_to_end(key)
        self.version[key] = self.counter
        heapq.heappush(self.expiry, (now + ttl, self.counter, key))
        if len(self.expiry) > 4 * self.cap + 16:   # 覆盖写留下的失效堆项太多时重建堆
            self.expiry = [(e, self.version[k], k) for k, (_, e) in self.data.items()]
            heapq.heapify(self.expiry)

    def _drop(self, key: int) -> None:
        del self.data[key]
        del self.version[key]

    def _purge_expired(self, now: float) -> None:
        while self.expiry and self.expiry[0][0] <= now:
            _, ver, key = heapq.heappop(self.expiry)
            if self.version.get(key) == ver:   # 版本对得上才是当前条目，否则是被覆盖或淘汰的旧堆项
                self._drop(key)
```
