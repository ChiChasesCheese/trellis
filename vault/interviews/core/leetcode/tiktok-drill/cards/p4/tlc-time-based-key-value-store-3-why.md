---
id: tlc-time-based-key-value-store-3-why
node: p4.time-based-key-value-store
type: qa
step: 3
---
## Q
**LC 981 基于时间的键值存储**｜正确性

`get` 里为什么用 `bisect_right` 再减一，而不是 `bisect_left`？为什么还要单独处理 `i == 0`？

## A
**不变量。** 同一个键的 `times` 列表严格递增。`i = bisect_right(times, t)` 满足：`times[:i]` 全部 `<= t`，`times[i:]` 全部 `> t`。所以 `times[i-1]` 就是不超过 `t` 的最大时间戳。

**为什么是 `bisect_right`。** 题目要求「`timestamp_prev <= timestamp`」，等号要算在内。`bisect_right` 把等于 `t` 的元素放在返回位置的左边，`i - 1` 恰好取到它；`bisect_left` 把它放在返回位置的右边，`i - 1` 取到的是更早的版本。

**反例：`bisect_left`。** 存了 `(1, "bar")` 和 `(4, "bar2")`，查询 `get("foo", 4)`：
- `times = [1, 4]`，`bisect_left(times, 4) = 1`，`i - 1 = 0`，返回 `"bar"`，错误。
- `bisect_right(times, 4) = 2`，`i - 1 = 1`，返回 `"bar2"`，正确。

**为什么处理 `i == 0`。** 所有已存的时间戳都大于查询时间时，`bisect_right` 返回 `0`。`values[-1]` 在 Python 里是最后一个元素，不会报错，会悄悄返回最新的值。`get("foo", 0)` 应当返回 `""`，如果不判断 `i`，会错成 `"bar2"`。
