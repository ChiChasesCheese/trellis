---
id: tlc-tt-lru-cache-ttl-0-whole
node: a.tt-lru-cache-ttl
type: qa
---
## Q
**带 TTL 的 LRU 缓存**｜Hard · 近一年被问：美国 14 次、国内 27 次 · 最近 2026-10（面试记录）

设计固定容量 `capacity` 的 LRU 缓存，接口 `get(key) -> value | -1` 与 `put(key, value, ttl)`。每次 `put` 传入这一条的存活时间 `ttl`（秒，不同条目可以不同）：
1. 写入后经过 `ttl` 就视为过期；`get` 读到过期条目时当作不存在：删除它并返回 `-1`（懒删除，不要后台线程）。
2. `put` 已存在的 key：覆盖 value、重置 `ttl`、变成最近使用。
3. 容量已满且要插入新 key：先清掉所有已过期的条目，仍满再淘汰最久未使用的条目。

`get` 与 `put` 要求 `O(1)`（均摊）。`1 <= capacity <= 10^5`，`ttl > 0`，key 和 value 是整数，时间来自一个可注入的 `clock()`。例：容量 `2`，`put(1, 1, ttl=5)`、`put(2, 2, ttl=10)`，`get(1)` → `1`；`put(3, 3, ttl=10)` 淘汰 key 2，`get(2)` → `-1`；时间走到 `6` 秒后 `get(1)` → `-1`（已过期）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用 `OrderedDict`（哈希表 + 双向链表）存 `key -> (value, 到期时刻)` 并按最近使用排序；`get` 时懒检查过期；`put` 满了先清过期、再淘汰队首；「清所有过期」靠一个按到期时刻排序的最小堆，每个堆项带写入版本号，被覆盖或淘汰后留下的旧堆项弹出时直接丢弃。

**识别。** 「固定容量 + 淘汰最久未用 + `get`/`put` 都 `O(1)`」就是 LRU：哈希表管查找，双向链表管移动和淘汰。TTL 是叠加的第二个淘汰维度：读路径只碰一个 key，当场检查即可；「满了先清过期」要找出**所有**过期条目，而链表按使用顺序排、不按到期顺序排，所以还要一个按到期时刻排序的结构。

**推导。** 暴力：满的时候遍历全部条目找过期的，每次 `put` 都 `O(n)`。浪费：过期的只可能是到期时刻最小的那些，却每次全扫。洞察：用最小堆按到期时刻排序，只看堆顶，`<= now` 就弹出，每个条目至多进出堆各一次，均摊 `O(log n)`。堆不支持随机删除，覆盖写和淘汰会留下失效的旧堆项：给每次写入一个递增版本号，弹出时和 `version[key]` 比，对不上就是旧项，丢掉。覆盖写多了堆会膨胀，超过 `4 * capacity + 16` 项时按当前数据重建。

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

运行（假时钟，时间记作 `t`）：容量 `2`，`put(1, 1, 5)`、`put(2, 2, 10)`，`get(1)` → `1`；`put(3, 3, 10)` 淘汰 key 2，`get(2)`、`get(3)` → `-1`、`3`；`t = 6` 时 `get(1)` → `-1`。另一组：容量 `2`，`t = 0` 时 `put(1, 1, 1)`、`put(2, 2, 100)`、`get(1)`，`t = 2` 时 `put(3, 3, 100)`：满了先清掉已过期的 key 1，`get(1)`、`get(2)`、`get(3)` → `-1`、`2`、`3`。

**复杂度。** `get` 为 `O(1)`；`put` 均摊 `O(log n)`（每个条目至多入堆、出堆各一次）；空间 `O(capacity)`。

**易错点。**
- 满了要先清过期、再淘汰：直接淘汰最久未用，会踢掉一个还活着的条目，而过期条目继续占位。上面第二组若跳过清理，`get(2)` 会得到 `-1`，正确是 `2`。
- 只有「新 key 且已满」才腾位置：覆盖写已有 key 也检查容量，会白白淘汰别人。容量 `2` 存着 key 1、2，`put(2, 9, 5)` 误淘汰 key 1，`get(1)` 得到 `-1`，正确是原值。
- 堆项必须带版本号：容量 `2`，`put(1, 1, ttl=1)`、`put(1, 2, ttl=100)`、`put(9, 9, ttl=100)`、`get(1)`，`t = 2` 时 `put(3, 3, ttl=100)`：旧堆项弹出时只看 key，会删掉还活着的 key 1，`get(1)` 得到 `-1`，正确是 `2`（被淘汰的是 key 9）。

**追问。**
- LFU：每个访问次数一个 `OrderedDict`，记 `min_freq`；过期清理仍然靠堆。
- 加权 LRU：容量按总权重算，把「淘汰一个」改成 `while 总权重 + 新权重 > capacity` 循环淘汰。
- 线程安全：`get` 会改使用顺序，读写锁没用；一把 `threading.Lock`，或按 `hash(key) % N` 分段加锁。

**同模式。** LC 146 LRU 缓存、LC 460 LFU 缓存、LC 432 全 `O(1)` 的数据结构、LC 981 基于时间的键值存储。
