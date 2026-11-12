---
slug: minimum-interval-to-include-each-query
---
## Q
**LC 1851 包含每个查询的最小区间**｜Hard

对每个查询 `q`，求包含 `q` 的所有闭区间中长度（`right - left + 1`）最小的，没有则为 `-1`。

## A
**一句话。** 离线处理：查询从小到大，左端点已 `<= q` 的区间入小根堆（长度, 右端点），堆顶够不着 `q` 的丢掉，堆顶就是答案。

```python
def min_interval(intervals, queries):
    intervals.sort()
    ans = [-1] * len(queries)
    heap, i = [], 0               # 堆里是 (长度, 右端点)
    order = sorted((q, k) for k, q in enumerate(queries))
    for q, qi in order:
        while i < len(intervals) and intervals[i][0] <= q:
            l, r = intervals[i]
            heappush(heap, (r - l + 1, r))
            i += 1
        while heap and heap[0][1] < q:   # 以后更大的 q 也够不着
            heappop(heap)
        if heap:
            ans[qi] = heap[0][0]
    return ans
```

**复杂度。** 时间 `O((n + q) log(n + q))`，空间 `O(n + q)`。

**易错点。**
- 按原顺序处理查询：丢弃的区间对后面较小的查询仍有用，`queries=[5,2]` 得 `[4,4]`，应为 `[4,3]`。
- 长度写成 `r - l`：示例一得 `[2,2,0,3]`，应为 `[3,3,1,4]`。
- 不弹出右端点 `< q` 的堆顶：`[1,1]` 对 `q=2` 会被误当作覆盖。

**追问。**
- 为什么丢弃是安全的？：查询递增，右端点 `< q` 的区间对之后所有查询都够不着。
- 在线查询怎么做？：不能排序查询，改用离散化加线段树，区间取 min。

**同模式。** LC 56 合并区间、LC 253 会议室 II、LC 218 天际线问题、LC 435 无重叠区间
