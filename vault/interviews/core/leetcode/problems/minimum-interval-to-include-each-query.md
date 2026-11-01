---
slug: minimum-interval-to-include-each-query
---
## Q
**LC 1851 包含每个查询的最小区间（Minimum Interval to Include Each Query）**｜Hard

给你二维整数数组 `intervals`，其中 `intervals[i] = [lefti, righti]` 表示第 `i` 个区间开始于 `lefti`、结束于 `righti`（闭区间）。区间的长度定义为区间中包含的整数数目，即 `righti - lefti + 1`。再给你整数数组 `queries`。第 `j` 个查询的答案是满足 `lefti <= queries[j] <= righti` 的长度最小区间的长度；如果不存在这样的区间，答案是 `-1`。以数组形式返回对应查询的所有答案。`1 <= intervals.length <= 10^5`，`1 <= queries.length <= 10^5`，`intervals[i].length == 2`，`1 <= lefti <= righti <= 10^7`，`1 <= queries[j] <= 10^7`。例：`intervals = [[1,4],[2,4],[3,6],[4,4]]`，`queries = [2,3,4,5]` → `[3,3,1,4]`；`intervals = [[2,3],[2,5],[1,8],[20,25]]`，`queries = [2,19,5,22]` → `[2,-1,4,6]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 离线查询（offline queries）+ 排序 + 小根堆 + 惰性删除（lazy deletion）。

**一句话。** 查询从小到大处理：把左端点已经 `<=` 当前查询的区间按（长度，右端点）放进小根堆，堆顶右端点小于查询的区间永久丢弃，剩下的堆顶就是最短的覆盖区间。

**识别。** 「很多区间 × 很多查询点，问覆盖点的最短区间」，`10^5 × 10^5` 不能逐个比较；查询可以重排顺序（答案按下标写回），说明离线 + 排序扫描线（sweep line）。

**推导。** 每个查询扫全部区间 `O(nq)`，`10^10` 超时。把查询按值升序：区间只要左端点 `<= q` 就可能覆盖 `q`，而且之后更大的查询仍满足这个条件，所以每个区间只需要入堆一次。堆按长度排序，求最短只看堆顶。区间是否真的覆盖 `q` 还要右端点 `>= q`；查询递增，右端点 `< q` 的区间对当前和之后所有查询都已无效，可以永久丢弃。丢弃只在堆顶发生也够：过期但没在堆顶的区间长度更大，不影响最小值，等它浮到堆顶再丢（惰性删除）。

```python
import heapq


def min_interval(intervals: list[list[int]], queries: list[int]) -> list[int]:
    intervals = sorted(intervals)                 # 按左端点升序
    ans = [-1] * len(queries)
    heap: list[tuple[int, int]] = []              # 小根堆 (长度, 右端点)：左端点已经 <= 当前查询的区间
    i = 0
    for qi in sorted(range(len(queries)), key=queries.__getitem__):   # 查询从小到大处理，答案按原下标写回
        q = queries[qi]
        while i < len(intervals) and intervals[i][0] <= q:
            left, right = intervals[i]
            heapq.heappush(heap, (right - left + 1, right))
            i += 1
        while heap and heap[0][1] < q:            # 堆顶右端点 < q：它够不着 q，也够不着之后更大的查询，永久丢弃
            heapq.heappop(heap)
        if heap:
            ans[qi] = heap[0][0]                  # 堆里剩下的都满足 left <= q <= right，取最短的
    return ans
```

运行：示例一 → `[3, 3, 1, 4]`，示例二 → `[2, -1, 4, 6]`，`([[1,1]], [2])` → `[-1]`。

**复杂度。** 时间 `O((n + q) log (n + q))`，空间 `O(n + q)`。

**易错点。**
- 按原顺序处理查询：丢弃的区间对后面较小的查询仍然有用。`intervals = [[1,4],[2,4],[3,6],[4,4]]`，`queries = [5, 2]` 得到 `[4, 4]`，正确 `[4, 3]`。
- 长度写成 `right - left`：示例一得到 `[2, 2, 0, 3]`，正确 `[3, 3, 1, 4]`。
- 只比较长度不判断右端点：堆顶可能是左端点 `<= q` 但右端点 `< q` 的区间（比如 `[1,1]` 对 `q = 2`），会误当作覆盖。

**同模式。** LC 56 合并区间、LC 253 会议室 II、LC 218 天际线问题、LC 435 无重叠区间。
