---
slug: minimum-initial-energy-to-finish-tasks
---
## Q
**LC 1665 完成所有任务的最少初始能量**｜Hard

任务 `[actual, minimum]`：开始前能量至少 `minimum`，完成后消耗 `actual`。任务顺序任选，求最少的初始能量。

## A
**一句话。** 按 `minimum - actual` 从大到小做（交换论证）；按这个顺序，初始能量要满足每个任务开始时「已花能量 + 门槛」，取最大值。

```python
def minimum_effort(tasks):
    # 门槛与消耗之差大的先做
    tasks.sort(key=lambda t: t[1] - t[0], reverse=True)
    ans = spent = 0
    for a, m in tasks:
        ans = max(ans, spent + m)  # 开始前剩余 >= m
        spent += a
    return ans
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`（不计排序）。

**易错点。**
- 按门槛 `minimum` 从大到小排序：`[[1,3],[3,4]]` 中门槛差 2 的应先做，按门槛排序会多要能量。
- 答案取 `sum(actual)`：还要满足每一步的门槛，取的是各步要求的最大值。

**追问。**
- 交换论证怎么做？：相邻两个任务 `x`、`y`，先 `x` 的要求是 `max(mx, ax + my)`，先 `y` 是 `max(my, ay + mx)`；`mx - ax > my - ay` 时先 `x` 不更差。
- 二分答案？：二分初始能量，按同样顺序模拟检查，`O(n log U)`，但排序依据还是一样。

**同模式。** LC 621 任务调度器、LC 1029 两地调度、LC 2136 全部开花的最早一天
