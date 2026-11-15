---
slug: two-best-non-overlapping-events
---
## Q
**LC 2054 两个最好的不重叠活动**｜Medium

活动 `[start, end, value]`，起止时刻都包含在内。最多选两个时间不重叠的活动（第二个必须在 `end + 1` 或之后开始），求价值和的最大值。

## A
**一句话。** 按开始时间排序，预处理后缀最大价值；枚举第一个活动，二分找第一个开始时间 `> end` 的活动，加上那里的后缀最大值。

```python
def max_two_events(events):
    events.sort()
    starts = [s for s, _, _ in events]
    n = len(events)
    suf = [0] * (n + 1)      # suf[i]：第 i 个及之后的最大价值
    for i in range(n - 1, -1, -1):
        suf[i] = max(suf[i + 1], events[i][2])
    ans = 0
    for s, e, v in events:
        j = bisect_right(starts, e)   # 第一个开始 > e 的
        ans = max(ans, v + suf[j])    # suf[n] = 0：只选一个
    return ans
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 用 `bisect_left`：开始时间等于 `e` 的活动也被算作不重叠，但端点包含在内，算重叠。
- 忘了只选一个的情况：`suf[n] = 0` 正好兜住。

**追问。**
- 最多选 `k` 个？：按结束时间排序做 `f[i][j]`，二分找前驱，就是 LC 1751。
- 不二分？：按时间扫描线，把开始和结束拆成事件，结束先于开始处理，维护已结束活动的最大价值。

**同模式。** LC 435 无重叠区间、LC 1235 规划兼职工作、LC 2008 出租车的最大盈利、LC 1751 最多可以参加的会议数目 II
