---
id: tlc-non-overlapping-intervals-4-followup
node: p4.non-overlapping-intervals
type: qa
step: 4
---
## Q
**LC 435 无重叠区间**｜追问

面试官接着问：（1）要返回具体被移除的是哪些区间；（2）每个区间有权重，要保留总权重最大的一组不重叠区间；（3）「端点接触也算重叠」时要改哪里？

## A
1. **列出被移除的区间**：贪心不变，把进不了 `if start >= end` 的区间收进列表。`[[1,2],[2,3],[3,4],[1,3]]` 得到 `[[1,3]]`，`[[1,2],[1,2],[1,2]]` 得到两个 `[1,2]`。
2. **带权重**：贪心失效（短区间权重可能很小），改成 DP：按右端点排序，`dp[i]` 是前 `i` 个区间的最大权重，用二分找最后一个右端点 `<= start` 的区间。`O(n log n)`。

```python
from bisect import bisect_right


def max_weight(intervals: list[tuple[int, int, int]]) -> int:   # (start, end, weight)
    iv = sorted(intervals, key=lambda x: x[1])
    ends = [e for _, e, _ in iv]
    dp = [0] * (len(iv) + 1)                  # dp[i]：前 i 个区间能得到的最大权重
    for i, (s, e, w) in enumerate(iv):
        j = bisect_right(ends, s, 0, i)       # 右端点 <= s 的区间个数，它们都能排在当前区间前面
        dp[i + 1] = max(dp[i], dp[j] + w)     # 不选当前区间 / 选当前区间
    return dp[-1]
```

`[(1,3,5),(2,4,6),(3,5,5),(4,6,4)]` → `10`。
3. **接触也算重叠**：条件改成 `start > end`，就是 LC 452 引爆气球；`[[1,2],[2,3]]` 此时只能保留一个。

**Python 提醒**：`bisect_right(ends, s, 0, i)` 的 `hi=i` 把搜索范围限制在已处理的前 `i` 个区间；`bisect_right` 保证右端点恰好等于 `s` 的区间也算在内，对应「接触不重叠」，换成 `bisect_left` 会把它们排除。
