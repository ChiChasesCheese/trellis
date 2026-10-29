---
id: uth-compose-singleflight-5-interview
node: compose.singleflight
type: qa
step: 5
---
## Q
**借到面试题：给 LRU 缓存加回源合并**｜singleflight · TTL LRU 缓存

面试官追问带 TTL 的 LRU 缓存：大批 key 同时过期，请求同时回源，怎么办？

## A
**背景。** 带 TTL 的 LRU 缓存只管存和淘汰；追问里的"回源请求合并"就是 singleflight：缓存前面加一张"正在回源的 key → 调用"表。

**结构。** 加一个 `get_or_load`：先查缓存；没命中就进 `Group.do(key, load)`；`load` 里先再查一次缓存（前一个回源者可能刚写好），仍没有才调用 loader 并写回缓存。

```python
def get_or_load(self, key: int, loader: Callable[[int], int], ttl: float) -> int:
    value = self.get(key)                     # 1. 先查缓存
    if value != -1:
        return value

    def load() -> int:                        # 2. 未命中：同一个 key 同时只回源一次
        value = self.get(key)                 # 3. 再查一次：前一个回源者可能刚写好
        if value == -1:
            value = loader(key)
            self.put(key, value, ttl)         # 4. 写回缓存，要在 do 里面完成
        return value

    return self.flight.do(str(key), load)     # flight 是 __init__ 里建的 Group()
```

**坑。** 写回缓存放在 `do` 外面，下一批请求会在写入之前又去回源。例题里的 `LRUCacheTTL` 本身不是线程安全的，多线程使用要加锁，`get`、`put` 都要在锁内。

**例题：** 带 TTL 的 LRU 缓存

设计固定容量的 LRU 缓存：`get(key)` 返回值或 `-1`，`put(key, value, ttl)` 写入并设置存活时间；读到过期条目当作不存在并删除；容量满了要插入新 key 时，先清掉所有过期条目，仍满再淘汰最久未使用的。时间来自可注入的 `clock()`。例：容量 2，`put(1,1,ttl=5)`、`put(2,2,ttl=10)`，`get(1)` → `1`；`put(3,3,ttl=10)` 淘汰 key 2，`get(2)` → `-1`；时间走到 6 秒后 `get(1)` → `-1`。

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
