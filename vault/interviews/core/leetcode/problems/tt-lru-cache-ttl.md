---
slug: tt-lru-cache-ttl
---
## Q
**带 TTL 的 LRU 缓存**｜Hard

设计容量 `capacity` 的 LRU 缓存：`get(key)` 返回值或 `-1`，`put(key, value, ttl)` 的每条数据有自己的存活时间。过期条目读到时懒删除并返回 `-1`；满了且要插入新 key 时，先清掉所有过期条目，仍满再淘汰最久未用。`get`、`put` 均摊 `O(1)`，时间来自可注入的 `clock()`。

## A
**一句话。** `OrderedDict` 按最近使用排序存 `(值, 到期时刻)`，另用到期时刻最小堆批量清过期，堆项带写入版本号，旧堆项弹出时丢弃。

```python
class LRUCacheTTL:
    def __init__(self, capacity, clock=time.monotonic):
        self.cap = capacity
        self.clock = clock
        self.data = OrderedDict()   # key -> (值, 到期)，队尾最新
        self.expiry = []            # 堆：(到期, 版本, key)
        self.version = {}           # key -> 当前有效版本
        self.counter = 0

    def get(self, key):
        item = self.data.get(key)
        if item is None:
            return -1
        value, expire_at = item
        if self.clock() >= expire_at:   # 懒删除
            self._drop(key)
            return -1
        self.data.move_to_end(key)
        return value

    def put(self, key, value, ttl):
        now = self.clock()
        full = len(self.data) >= self.cap
        if key not in self.data and full:
            self._purge(now)            # 先清过期
            if len(self.data) >= self.cap:
                self._drop(next(iter(self.data)))  # 再淘汰最旧
        self.counter += 1
        self.data[key] = (value, now + ttl)
        self.data.move_to_end(key)
        self.version[key] = self.counter
        heapq.heappush(self.expiry,
                       (now + ttl, self.counter, key))
        if len(self.expiry) > 4 * self.cap + 16:  # 旧堆项太多
            self.expiry = [(e, self.version[k], k) for k,
                           (_, e) in self.data.items()]
            heapq.heapify(self.expiry)

    def _drop(self, key):
        del self.data[key]
        del self.version[key]

    def _purge(self, now):
        while self.expiry and self.expiry[0][0] <= now:
            _, ver, key = heapq.heappop(self.expiry)
            if self.version.get(key) == ver:  # 否则是旧堆项
                self._drop(key)
```

**复杂度。** 时间 `get` 为 `O(1)`、`put` 均摊 `O(log n)`，空间 `O(capacity)`。

**易错点。**
- 满了直接淘汰、不先清过期：会踢掉还活着的条目，过期的继续占位。
- 覆盖写已有 key 也腾位置：容量 `2` 存着 key 1、2，`put(2, 9, 5)` 误淘汰了 key 1。
- 堆项不带版本号：`put(1,..,ttl=1)` 再 `put(1,..,ttl=100)`，旧堆项弹出时会误删还活着的 key 1。

**追问。**
- 改成 LFU？：每个访问次数一个 `OrderedDict` 并记 `min_freq`，过期清理仍靠堆。
- 线程安全？：`get` 会改使用顺序，读写锁没用；用一把锁，或按 `hash(key)` 分段加锁。

**同模式。** LC 146 LRU 缓存、LC 460 LFU 缓存、LC 981 基于时间的键值存储、LC 432 全 O(1) 的数据结构
