---
slug: time-based-key-value-store
---
## Q
**LC 981 基于时间的键值存储**｜Medium

设计 `TimeMap`：`set(key, value, timestamp)` 存值（时间戳严格递增），`get(key, timestamp)` 返回时间戳不超过它的最新值，没有则返回 `""`。

## A
**一句话。** 每个键存两个并行的递增列表，`set` 直接追加，`get` 在时间戳列表上二分。

```python
class TimeMap:
    def __init__(self):
        self.times = defaultdict(list)    # key -> 递增时间戳
        self.values = defaultdict(list)   # key -> 同下标的值

    def set(self, key, value, timestamp):
        self.times[key].append(timestamp)   # 严格递增，天然有序
        self.values[key].append(value)

    def get(self, key, timestamp):
        times = self.times.get(key)       # 不用 []，免得造出空列表
        if not times:
            return ""
        i = bisect_right(times, timestamp)  # 第一个 > 的位置
        return self.values[key][i - 1] if i else ""
```

**复杂度。** 时间 `set` 均摊 `O(1)`，`get` `O(log m)`，空间 `O(S)`。

**易错点。**
- 用 `bisect_left`：`times=[1,4]` 查 `4` 会落在前面，取到旧值 `"bar"`，应为 `"bar2"`。
- 忘了 `i == 0`：`values[-1]` 是负下标，悄悄返回最后一个值而不是 `""`。
- `get` 里写 `self.times[key]`：`defaultdict` 会为不存在的键造出空列表。

**追问。**
- 时间戳不保证递增？：`set` 用 `insort` 保持有序，插入 `O(m)`；要 `O(log m)` 需平衡树或 `SortedList`。
- 内存吃紧？：只保留最近 `N` 个版本，或把旧版本落盘，内存里留索引。

**同模式。** LC 1146 快照数组、LC 729 我的日程安排 I、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 2034 股票价格波动
