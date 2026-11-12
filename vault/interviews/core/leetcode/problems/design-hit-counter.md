---
slug: design-hit-counter
---
## Q
**LC 362 敲击计数器**｜Medium

设计一个敲击计数器，统计过去 5 分钟（300 秒）内收到的敲击次数。实现类 `HitCounter`：`hit(timestamp)` 在第 `timestamp` 秒记录一次敲击（同一秒可以有多次）；`getHits(timestamp)` 返回 `(timestamp - 300, timestamp]` 这段时间内的敲击次数。所有调用按时间顺序给出（`timestamp` 单调不减），`1 <= timestamp <= 2 * 10^9`，最多调用 `300` 次 `hit` 和 `getHits`。例：`hit(1)`、`hit(2)`、`hit(3)`，`getHits(4)` → `3`，`hit(300)`，`getHits(300)` → `4`，`getHits(301)` → `3`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 滑动时间窗口（sliding window）+ 队列（`deque`）：时间戳单调不减，过期的敲击一定在队头。

**一句话。** 每次敲击把时间戳追加到队尾，查询时先从队头弹掉已过期的，剩下的长度就是答案。

**识别。** 「过去一段时间内的计数」+ 「调用按时间顺序」= 窗口只会向右滑，用队列弹出过期项，每个时间戳最多进出一次，均摊 `O(1)`。

**推导。** 暴力：存下所有时间戳，查询时整个扫一遍，`O(n)`，并且内存一直涨。窗口左边界只增不减，过期的永远不会再有用，所以边查边丢；因为输入有序，队头就是最老的，不用排序也不用堆。

```python
from collections import deque


class HitCounter:
    def __init__(self) -> None:
        # 每次敲击的时间戳，调用本身有序，所以队列天然升序
        self.hits: deque[int] = deque()

    def hit(self, timestamp: int) -> None:
        self.hits.append(timestamp)  # 同一秒多次敲击就存多份

    def getHits(self, timestamp: int) -> int:
        # 窗口是 (t-300, t]：差值 >= 300 的已过期
        while self.hits and self.hits[0] <= timestamp - 300:
            self.hits.popleft()
        return len(self.hits)
```

运行：示例依次得到 `3`、`4`、`3`；空计数器 `getHits(5)` → `0`；`hit(1)`、`hit(301)` 后 `getHits(301)` → `1`；同一秒敲击 `5` 次，`getHits(306)` → `5`，`getHits(307)` → `0`。

**复杂度。** `hit` 为 `O(1)`，`getHits` 均摊 `O(1)`；空间 `O(窗口内的敲击数)`。

**拓展优化。**
- 每秒敲击量极大时队列会存下成千上万份：按秒聚合成 300 个桶的环形数组，内存固定 `O(300)`，`getHits` 是 `O(300)`：

```python
class HitCounterRing:
    def __init__(self) -> None:
        self.times = [0] * 300   # times[i]：槽 i 当前代表的那一秒
        self.counts = [0] * 300  # counts[i]：那一秒的敲击数

    def hit(self, timestamp: int) -> None:
        i = timestamp % 300
        # 槽里是 300 秒前的旧数据：先清零再记
        if self.times[i] != timestamp:
            self.times[i], self.counts[i] = timestamp, 0
        self.counts[i] += 1

    def getHits(self, timestamp: int) -> int:
        pairs = zip(self.times, self.counts)
        return sum(c for t, c in pairs if timestamp - t < 300)
```

- 多线程：`hit` 和 `getHits` 共用一把锁；更高并发时每个槽一把锁或原子计数，分布式时各机器各自计数再相加。

**易错点。**
- 边界写成 `<`（`self.hits[0] < timestamp - 300`）：示例里 `getHits(301)` 会返回 `4`，正确是 `3`，因为 `301 - 1 = 300` 已经不在 `(1, 301]` 里。
- 环形数组忘记检查槽里的旧时间戳：`hit(1)` 之后 `hit(301)` 落在同一个槽，不清零的话这一秒会被记成 `2` 次。
- 同一秒多次敲击要各算一次，不要用集合存时间戳。

**追问。**
- 每秒上百万次敲击怎么办？队列版内存随敲击数涨，改用环形桶，内存固定 `O(300)`，`hit` 是 `O(1)`，`getHits` 是 `O(300)`，与流量无关。
- `getHits` 能不能也 `O(1)`？维护一个总数 `total`：`hit` 加一；过期时（弹队头或覆盖旧槽）减去对应计数，整体仍是均摊 `O(1)`，代价是每次要先清理过期槽，环形版需要按时间推进清理中间跳过的槽。
- 窗口长度可变（如查询过去 `w` 秒）？队列版二分查最早未过期的位置（时间戳有序），`O(log n)`，同时不能再边查边丢。
- 多机器分布式？各机器各自计数，查询时汇总，或把每秒计数写进共享存储（如 Redis 的有序集合）按分钟分片。

**同模式。** LC 359 日志速率限制器、LC 933 最近的请求次数、LC 346 数据流中的移动平均值、LC 1797 设计一个验证系统。
