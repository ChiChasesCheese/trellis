---
id: tlc-maximum-number-of-events-that-can-be-attended-0-whole
node: c.maximum-number-of-events-that-can-be-attended
type: qa
---
## Q
**LC 1353 最多可以参加的会议数目**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 4 次 · 最近 2021-07-28（国内 CodeTop）

给你一个数组 `events`，`events[i] = [startDayi, endDayi]` 表示会议 `i` 开始于 `startDayi`、结束于 `endDayi`。你可以在满足 `startDayi <= d <= endDayi` 的任意一天 `d` 参加会议 `i`，且任意一天只能参加一场会议。返回你可以参加的最大会议数目。`1 <= events.length <= 10^5`，`events[i].length == 2`，`1 <= startDayi <= endDayi <= 10^5`。例：`events = [[1,2],[2,3],[3,4]]` → `3`；`events = [[1,2],[2,3],[3,4],[1,2]]` → `4`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 按天往后走，每天把当天开始的会议的结束日放进最小堆，丢掉已过期的，然后参加结束日最早的那个会议（最早截止优先），`O(n log n)`。

**识别。** 「每个任务有可选的时间窗口、每个时间槽只能做一个、求最多做几个」是带释放时间和截止时间的单位任务调度，贪心是最早截止优先（EDF）。

**推导。** 暴力：枚举每个会议参加哪一天，指数级。贪心的论证：某一天面对若干可参加的会议，优先参加结束最早的，因为结束晚的会议将来还有更多天可选，而结束早的这一天不选就永远错过；交换论证可证明不会更差。实现：`day` 指针往前走，开始日 `<= day` 的会议结束日入堆；堆顶若 `< day` 已过期，弹掉；堆非空则弹出堆顶参加，计数加一；`day` 加一。堆空时直接跳到下一个会议的开始日。

```python
from heapq import heappop, heappush


def max_events(events: list[list[int]]) -> int:
    events = sorted(events)                      # 按开始日升序
    heap: list[int] = []                         # 当前可参加的会议的结束日（最小堆）
    i, n = 0, len(events)
    day = count = 0
    while i < n or heap:
        if not heap:
            day = events[i][0]                   # 没有可参加的会议：直接跳到下一个开始日
        while i < n and events[i][0] <= day:
            heappush(heap, events[i][1])         # 今天开始的会议入堆，按结束日排序
            i += 1
        while heap and heap[0] < day:
            heappop(heap)                        # 已经过期的会议扔掉
        if heap:
            heappop(heap)                        # 参加结束最早的那个
            count += 1
        day += 1
    return count
```

运行：`[[1,2],[2,3],[3,4]]` → `3`，`[[1,2],[2,3],[3,4],[1,2]]` → `4`；`[[1,1],[1,1],[1,1]]` → `1`，`[[1,5],[1,5],[1,5],[2,3],[2,3]]` → `5`，`[[1,100000]] * 100000` → `100000`。

**复杂度。** 时间 `O(n log n)`（排序加堆操作，每个会议入堆、出堆至多一次，`day` 每次要么参加会议要么跳转）；空间 `O(n)`。

**拓展优化。**
- 另一种贪心：按结束日升序，每个会议占窗口里最早的空闲日，用并查集（Union-Find）的 `find` 直接跳到空闲日，接近 `O(n α)`。

```python
def max_events_dsu(events: list[list[int]]) -> int:
    top = max(e for _, e in events) + 1
    nxt = list(range(top + 1))                   # nxt[d]：从 d 起（含）最早的空闲日

    def find(d: int) -> int:
        while nxt[d] != d:
            nxt[d] = nxt[nxt[d]]                 # 路径减半
            d = nxt[d]
        return d

    count = 0
    for start, end in sorted(events, key=lambda e: e[1]):
        d = find(start)
        if d <= end:                             # 窗口内还有空闲日
            count += 1
            nxt[d] = d + 1                       # d 被占用，下次直接跳到 d+1
    return count
```

**易错点。**
- 不丢弃过期会议：堆顶结束日小于今天的会议被算进去，`[[1,1],[1,1]]` 得到 `2`，正确是 `1`。
- 每天都固定 `day += 1` 而堆空时不跳转：稀疏的开始日（如 `[[1,1],[100000,100000]]`）会白跑大量空天，`day` 循环退化成按天数而非按会议数。
- 每天选开始日最早的会议（而不是结束日最早）：`[[2,4],[2,2],[2,3]]`（开始日相同取先出现的）得到 `2`，正确是 `3`。

**追问。**
- 每个会议有不同的权重、求总权重最大：不再是简单的贪心，是带权区间调度，通常改用 DP + 二分。
- 每天可以参加 `k` 场：每天从堆里弹 `k` 次。

**同模式。** LC 253 会议室 II、LC 435 无重叠区间、LC 452 用最少数量的箭引爆气球、LC 630 课程表 III、LC 1235 规划兼职工作。
