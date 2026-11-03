---
id: craft-unit-of-inventory-modeling-5-same-shape-everywhere
node: craft.architecture.unit-of-inventory-modeling
type: qa
step: 5
---
## Q
**库存的单位怎么选 · 会议室、酒店、SKU×仓库×时间，是同一个问题吗**｜架构

LeetCode 的会议室 II 问最少需要几间会议室；酒店订房问任意一晚会不会超过房量；库存系统要问某 SKU 在某仓在某段时间够不够。这三件事在建模上有什么共同点，单位怎么选决定了什么？

## A
**要点。** 共同点是容量约束沿着一个维度（时间）和若干维度（房型、仓库、SKU）展开：每个（维度组合，时间槽）一个格子，请求占用一段连续的格子，条件是每个格子都不超容量。会议室 II 的答案就是格子里最大的占用数；酒店的「整段能订几间」是整段里最紧那一晚剩余数的最小值；分布式库存是格子再加上仓库维度和分片。选的单位决定格子多细：夜、小时，还是具体某间房。

```python
meetings = [(0, 30), (5, 10), (15, 20), (10, 25)]       # (开始, 结束)，半开区间

def rooms_needed_heap(iv: list[tuple[int, int]]) -> int:
    """LeetCode 253 的标准解：小顶堆装「正在占用的会议结束时间」。"""
    ends: list[int] = []
    for s, e in sorted(iv):
        if ends and ends[0] <= s:
            heapq.heapreplace(ends, e)     # 有房间已空出：复用
        else:
            heapq.heappush(ends, e)        # 否则新开一间
    return len(ends)

def rooms_needed_by_night(iv: list[tuple[int, int]]) -> int:
    """酒店库存的写法：按「一晚」记已订数，最紧的那一晚就是需要的房间数。"""
    booked: dict[int, int] = {}
    for s, e in iv:
        for t in range(s, e):
            booked[t] = booked.get(t, 0) + 1
    return max(booked.values())

print("堆:", rooms_needed_heap(meetings), "| 按时间槽计数:", rooms_needed_by_night(meetings))
```

会议 `[(0,30), (5,10), (15,20), (10,25)]`，两种写法的实际输出：

```
堆: 3 | 按时间槽计数: 3
```

**为什么。** 两条路径等价：堆解法按时间顺序模拟「谁占着房」，按槽计数是直接统计每个时刻的并发数。槽计数的好处是每个格子独立，可以加锁、分片、做全有或全无的检查，放大到分布式时就是按 (SKU, 仓库, 时间槽) 分区；代价是格子数随时间跨度和粒度增长，需要定期清理过期格子。

**信号。** 看到「预订一段时间的有限资源」，先问单位：一个时间槽里谁在竞争，竞争的是哪个维度组合？单位选错的症状：需要大量特判才能表达「同一把椅子不同场次」「这辆车下周在哪」。
