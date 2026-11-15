---
slug: corporate-flight-bookings
---
## Q
**LC 1109 航班预订统计**｜Medium

有 `n` 个航班（编号 `1..n`）。每条预订 `[first, last, seats]` 表示为航班 `first` 到 `last`（含）各预订 `seats` 个座位。返回每个航班预订的座位总数。

## A
**一句话。** 差分数组：每条预订只在 `first` 处加、`last+1` 处减，最后做一次前缀和得到每个航班的总数。

```python
def corp_flight_bookings(bookings, n):
    diff = [0] * (n + 1)              # 多开一格放 last+1
    for first, last, seats in bookings:
        diff[first - 1] += seats      # 航班编号从 1 起，下标从 0 起
        diff[last] -= seats           # 即 last+1 对应的下标
    for i in range(1, n):
        diff[i] += diff[i - 1]        # 前缀和还原
    return diff[:n]
```

**复杂度。** 时间 `O(n + m)`，空间 `O(n)`。

**易错点。**
- 编号和下标差一：航班 `first` 对应下标 `first-1`，`last+1` 对应下标 `last`，别写成 `diff[last+1]`。
- 逐个航班累加：`O(n·m)` 会超时，差分把每条预订降为 `O(1)`。
- 最后忘了截掉多出的一格：返回前 `n` 项。

**追问。**
- 在线更新、随时查询怎么做？：差分不适合，改用树状数组或线段树。
- 这一类题的共同点？：区间加、最后一次性查询，就是差分的标准场景。

**同模式。** LC 370 区间加法、LC 1094 拼车、LC 2848 与车相交的点数、LC 253 会议室 II
