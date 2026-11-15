---
slug: maximum-number-of-events-that-can-be-attended-ii
---
## Q
**LC 1751 最多可以参加的会议数目 II**｜Hard

`events[i] = [开始日, 结束日, 价值]`，每场会议必须全程参加，两场会议的日期区间不能有重叠（结束日当天不能再开始另一场），至多参加 `k` 场。求能得到的最大价值总和。

## A
**一句话。** 按开始日排序，对每场会议选「参加」或「跳过」：参加就二分找到第一场开始日晚于它结束日的会议接着选，`k` 减一。

```python
def max_value(events, k):
    events.sort()
    starts = [e[0] for e in events]
    n = len(events)
    @cache
    def f(i, left):                    # 从第 i 场起，还能参加 left 场
        if i == n or left == 0:
            return 0
        nxt = bisect_right(starts, events[i][1])  # 下一场能参加的
        return max(f(i + 1, left),                # 不参加
                   f(nxt, left - 1) + events[i][2])   # 参加
    return f(0, k)
```

**复杂度。** 时间 `O(n·k·log n)`，空间 `O(n·k)`。

**易错点。**
- 二分用 `bisect_left`：结束日当天不能开始新会议，要找严格大于结束日的第一个，用 `bisect_right`。
- 贪心按价值或按结束日选：有 `k` 的限制，不能只看单个因素，要 DP。
- 没排序就二分：`starts` 必须有序。

**追问。**
- 事件数很大时递归会爆栈？：改成迭代 DP：`dp[j][i]` 按结束日排序后的前 `i` 场最多选 `j` 场的最大价值，二分找最后一个不冲突的。
- 不限制 `k` 时？：就是带权区间调度（LC 1235），去掉一维 `k`。

**同模式。** LC 1235 规划兼职工作、LC 2008 出租车的最大盈利、LC 1353 最多可以参加的会议数目
