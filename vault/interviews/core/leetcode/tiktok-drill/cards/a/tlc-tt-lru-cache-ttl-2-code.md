---
id: tlc-tt-lru-cache-ttl-2-code
node: a.tt-lru-cache-ttl
type: qa
step: 2
---
## Q
**带 TTL 的 LRU 缓存**｜写出 Python 实现

写一个类 `LRUCacheTTL(capacity, clock)`：`get(key)` 返回值或 `-1`（读到过期条目就删除并返回 `-1`）；`put(key, value, ttl)` 覆盖已有 key 时重置 `ttl` 并变成最近使用；新 key 且已满时先清过期条目，仍满再淘汰最久未使用的。`1 <= capacity <= 10^5`，`ttl > 0`，`clock` 返回当前秒数（默认 `time.monotonic`）。

## A
**思路。** `OrderedDict` 按使用顺序存 `key -> (value, 到期时刻)`，队首最久未用；一个按到期时刻排序的最小堆负责「找出全部过期条目」，堆项带写入版本号，覆盖或淘汰留下的旧项弹出时对不上版本就丢弃。

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

运行（假时钟，时间记作 `t`）：容量 `2`，`put(1, 1, 5)`、`put(2, 2, 10)`，`get(1)` → `1`；`put(3, 3, 10)` 淘汰 key 2，`get(2)`、`get(3)` → `-1`、`3`；`t = 6` 时 `get(1)` → `-1`；再 `put(1, 11, 2)`，`get(1)` → `11`，`t = 8` 时 `get(1)` → `-1`，`get(3)` → `3`。容量 `2`，`t = 0` 时 `put(1, 1, 1)`、`put(2, 2, 100)`、`get(1)`，`t = 2` 时 `put(3, 3, 100)` 后 `get(1)`、`get(2)`、`get(3)` → `-1`、`2`、`3`。`capacity = 3` 反复覆盖写 `10^5` 次后，堆长度仍只有 `4`。

**复杂度。** `get` 为 `O(1)`；`put` 均摊 `O(log n)`，每个条目至多入堆、出堆各一次，重建堆摊到每次写入是常数；空间 `O(capacity)`。

**写法要点。**
- `OrderedDict` 就是哈希表加双向链表：`move_to_end(key)` 与 `next(iter(d))`（取队首）都是 `O(1)`，不用手写节点。
- 时钟用 `time.monotonic`，不用 `time.time`：系统时间被校准或回拨时，墙钟会让条目提前或延后过期；把时钟作为构造参数，测试里用可控的假时钟。
- 过期用 `>=`：到期时刻那一瞬间就算过期，和堆里 `<= now` 的判断一致。
- 版本号加懒丢弃，代替「从堆里删除任意元素」：堆做不到 `O(log n)` 的随机删除，丢弃旧项的代价记在它自己的弹出上。
