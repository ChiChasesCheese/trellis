---
slug: maximum-number-of-events-that-can-be-attended
---
## Q
**LC 1353 最多可以参加的会议数目**｜Medium

`events[i] = [start, end]`，会议可在 `start..end` 中任意一天参加，每天最多一场。求最多能参加几场。

## A
**一句话。** 按天往后走，当天开始的会议结束日入最小堆，丢掉过期的，参加结束日最早的那场。

```python
def max_events(events):
    events = sorted(events)       # 按开始日
    heap = []                     # 可参加会议的结束日
    i, n = 0, len(events)
    day = count = 0
    while i < n or heap:
        if not heap:
            day = events[i][0]    # 无会可参加，跳到下一个开始日
        while i < n and events[i][0] <= day:
            heappush(heap, events[i][1])
            i += 1
        while heap and heap[0] < day:
            heappop(heap)         # 过期的扔掉
        if heap:
            heappop(heap)         # 参加结束最早的
            count += 1
        day += 1
    return count
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 不丢过期会议：`[[1,1],[1,1]]` 得 `2`，应为 `1`。
- 堆空时不跳转：`[[1,1],[100000,100000]]` 白跑大量空天。
- 选开始最早而非结束最早：`[[2,4],[2,2],[2,3]]` 可能只得 `2`，应为 `3`。

**追问。**
- 会议带权重求总权重最大？：不再是贪心，是带权区间调度，用 DP 加二分。
- 每天可参加 `k` 场？：每天从堆里弹 `k` 次。

**同模式。** LC 253 会议室 II、LC 435 无重叠区间、LC 630 课程表 III、LC 1235 规划兼职工作
