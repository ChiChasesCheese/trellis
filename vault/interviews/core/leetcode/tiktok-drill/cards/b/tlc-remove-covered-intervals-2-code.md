---
id: tlc-remove-covered-intervals-2-code
node: b.remove-covered-intervals
type: qa
step: 2
---
## Q
**LC 1288 删除被覆盖区间**｜写出 Python 实现

区间列表 `intervals`（长度 `1 ~ 1000`，端点在 `0 ~ 10^5`，互不相同），区间 `[a,b)` 若满足 `c <= a` 且 `b <= d` 就算被 `[c,d)` 覆盖。返回没有被任何其他区间覆盖的区间个数。

## A
**思路。** 按（起点升序，终点降序）排序。扫描时维护 `max_end`，表示排在前面的所有区间的最大终点。当前区间若终点不超过 `max_end`，说明前面某个区间起点不大于它、终点不小于它，被覆盖；否则保留，并把 `max_end` 更新为它的终点。

```python
def remove_covered_intervals(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda iv: (iv[0], -iv[1]))     # 起点升序；起点相同时长的在前
    kept = 0
    max_end = 0                                        # 目前见过的最大右端点
    for _, end in intervals:
        if end > max_end:                              # 右端点超过前面所有区间：没被覆盖
            kept += 1
            max_end = end
    return kept
```

运行：`[[1,4],[3,6],[2,8]]` → `2`，`[[1,2],[1,4]]` → `1`，`[[1,4],[2,3]]` → `1`，`[[1,2]]` → `1`，`[[0,1],[1,2],[2,3]]` → `3`。

**复杂度。** 时间 `O(n log n)`：排序主导，扫描 `O(n)`；空间 `O(1)`（原地排序，不计排序栈）。

**写法要点。** 排序键用元组 `(iv[0], -iv[1])`，一次排序同时表达「起点升序、终点降序」，不用写 `cmp` 函数。`for _, end in intervals` 解包时丢掉不需要的起点。`max_end` 初始为 `0` 是安全的，因为所有终点 `>= 1`。`list.sort()` 原地排序，比 `sorted` 少一次拷贝；如果不允许改动输入，用 `sorted(...)`。
