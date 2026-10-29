---
id: tlc-time-based-key-value-store-2-code
node: a.time-based-key-value-store
type: qa
step: 2
---
## Q
**LC 981 基于时间的键值存储**｜写出 Python 实现

实现 `TimeMap`：`set(key, value, timestamp)` 存值（同一个键的时间戳严格递增，`1 <= timestamp <= 10^7`）；`get(key, timestamp)` 返回时间戳不超过 `timestamp` 的最新值，没有则 `""`。`set` 与 `get` 合计最多 `2 * 10^5` 次。

## A
**思路。** 每个键保存两个并行列表：时间戳列表（递增）和值列表。`set` 追加到两个列表；`get` 在时间戳列表上 `bisect_right`，位置减一就是目标版本。

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

运行：`set("foo","bar",1)`；`get("foo",1)` → `'bar'`；`get("foo",3)` → `'bar'`；`set("foo","bar2",4)`；`get("foo",4)` → `'bar2'`；`get("foo",5)` → `'bar2'`；`get("foo",0)` → `''`；`get("nokey",1)` → `''`。

**复杂度。** `set` 均摊 `O(1)`；`get` `O(log m)`，`m` 是该键已有的版本数；空间 `O(S)`，`S` 是 `set` 的总次数。

**写法要点。** `defaultdict(list)` 让 `set` 不用先判断键是否存在，但 `get` 要用 `.get` 避免误建键；两个并行列表使 `bisect_right` 直接比较整数，比「元组列表 + `key=` 参数」更快；`i - 1` 配合 `if i else ""` 同时处理「没有任何版本不超过 `timestamp`」。Python 3.10 以后 `bisect` 也支持 `key=`，可写成 `bisect_right(pairs, timestamp, key=lambda p: p[0])`。
