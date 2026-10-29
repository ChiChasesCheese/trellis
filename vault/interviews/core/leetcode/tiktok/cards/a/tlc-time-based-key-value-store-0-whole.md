---
id: tlc-time-based-key-value-store-0-whole
node: a.time-based-key-value-store
type: qa
---
## Q
**LC 981 基于时间的键值存储**｜Medium · TikTok 高频

设计一个 `TimeMap` 类：同一个键在不同时间戳可以存多个值，并能按时间戳取值。`set(key, value, timestamp)` 在时间戳 `timestamp` 存入键 `key` 对应的值 `value`；`get(key, timestamp)` 返回此前某次 `set` 中满足 `timestamp_prev <= timestamp` 的值，若有多个，返回 `timestamp_prev` 最大的那个；没有则返回空串 `""`。`1 <= key.length, value.length <= 100`，由小写字母和数字组成，`1 <= timestamp <= 10^7`，所有 `set` 的时间戳**严格递增**，`set` 与 `get` 合计最多 `2 * 10^5` 次调用。例：`set("foo","bar",1)`；`get("foo",1)` → `"bar"`；`get("foo",3)` → `"bar"`；`set("foo","bar2",4)`；`get("foo",4)` → `"bar2"`；`get("foo",5)` → `"bar2"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 每个键存两个并行的递增列表（时间戳列表、值列表）；`set` 直接 `append`（时间戳严格递增，天然有序）；`get` 在时间戳列表上做 `bisect_right`，得到第一个大于 `timestamp` 的位置 `i`，答案就是下标 `i - 1`（`i == 0` 时返回空串）。`set` 均摊 `O(1)`，`get` 为 `O(log m)`。

**识别。** 「按时间取最近的历史版本」就是在有序序列里找**前驱**（不超过目标的最大元素），用二分。题目特意保证时间戳严格递增，这是关键条件：写入顺序就是时间顺序，不需要排序，也不需要在中间插入。`2 * 10^5` 次调用说明 `get` 不能线性扫描。

**推导。** 暴力：每个键存 `(时间戳, 值)` 列表，`get` 从后往前扫，最坏每次 `O(m)`，总 `O(n^2)`，`2 * 10^5` 次会超时 → 列表有序，前驱查询用二分，`O(log m)` → 把时间戳和值拆成两个并行列表，`bisect` 直接作用在纯整数列表上，比对元组列表加 `key` 函数更快 → `set` 不需要维护顺序，直接追加。

```python
from bisect import bisect_right
from collections import defaultdict


class TimeMap:
    def __init__(self) -> None:
        self.times: defaultdict[str, list[int]] = defaultdict(list)    # key -> 递增的时间戳
        self.values: defaultdict[str, list[str]] = defaultdict(list)   # key -> 与 times 同下标的值

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times[key].append(timestamp)       # 时间戳严格递增：直接 append 就是有序的
        self.values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        times = self.times.get(key)             # 用 .get：defaultdict 的 [] 会凭空造出空列表
        if not times:
            return ""
        i = bisect_right(times, timestamp)      # 第一个 > timestamp 的位置，i-1 就是最后一个 <= timestamp 的
        return self.values[key][i - 1] if i else ""
```

运行：`set("foo","bar",1)` 后 `get("foo",1)` → `'bar'`，`get("foo",3)` → `'bar'`；`set("foo","bar2",4)` 后 `get("foo",4)` → `'bar2'`，`get("foo",5)` → `'bar2'`，`get("foo",0)` → `''`，`get("nokey",1)` → `''`；十万次 `set` 加十万次 `get` 约 `0.02` 秒。

**复杂度。** `set` 均摊 `O(1)`；`get` `O(log m)`，`m` 是该键的版本数；空间 `O(S)`，`S` 是 `set` 的总次数。

**易错点。**
- 用 `bisect_left`：时间戳恰好等于某个存储值时会落在它前面。`times = [1, 4]` 查 `4`，`bisect_left` 得 `1`，减一后取到 `"bar"`；`bisect_right` 得 `2`，取到 `"bar2"`，才是正确的。
- 忘了 `i == 0`：`get("foo", 0)` 时 `i = 0`，`values[-1]` 是 Python 的负下标，会悄悄返回最后一个值而不是 `""`。
- 在 `get` 里用 `self.times[key]`：`defaultdict` 会为不存在的键创建空列表，查询一次就多一个键，污染数据。

**追问。**
- 时间戳不保证递增：`set` 时用 `bisect.insort` 保持有序，插入 `O(m)`（列表搬移）；要 `O(log m)` 的插入需要平衡树或跳表（Python 里常用第三方的 `sortedcontainers.SortedList`）。相同时间戳再次 `set` 要决定覆盖还是追加。
- 要删除、过期（TTL）：删除旧版本时，两个并行列表要同步删除；批量清理比逐个删高效。
- 版本特别多、内存吃紧：只保留最近 `N` 个版本，或者把旧版本落盘，内存里留索引。

**同模式。** LC 1146 快照数组、LC 729 我的日程安排 I、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 362 敲击计数器、LC 2034 股票价格波动。
