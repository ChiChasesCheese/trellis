---
id: tlc-block-placement-queries-5-alt
node: p5.block-placement-queries
type: qa
step: 5
---
## Q
**LC 3161 物块放置查询**｜另一种解法

不用线段树，最直接的做法是什么？它的复杂度是多少，适合多大的输入？

## A
**暴力：每次查询重新切段。** 用有序列表存障碍物。查询时取出 `<= x` 的所有障碍物，在末尾加上 `x`，相邻两点之间的距离就是 `[0, x]` 被切成的各段长度，取最大值与 `sz` 比较。

```python
from bisect import bisect_right, insort
from itertools import pairwise


def get_results(queries: list[list[int]]) -> list[bool]:
    obstacles = [0]                                 # 有序的障碍物位置，原点当哨兵
    ans: list[bool] = []
    for op, x, *rest in queries:
        if op == 1:
            insort(obstacles, x)
        else:
            cuts = obstacles[:bisect_right(obstacles, x)] + [x]   # [0, x] 被切成的各段端点
            ans.append(max(b - a for a, b in pairwise(cuts)) >= rest[0])
    return ans
```

`[[1,2],[2,3,3],[2,3,1],[2,2,2]]` → `[False, True, True]`。

**复杂度。** 每次查询 `O(k)`，`k` 是当前障碍物数，总计 `O(q · k)`。

**怎么选。**
- `q · k` 在 `10^7` 以内（几千条操作）：暴力足够，十行代码，几乎不会写错。
- 题目的上限 `1.5 * 10^5` 条、`5 * 10^4` 个障碍物：约 `10^9` 次以上操作，超时，必须用线段树（在线）或离线倒序加树状数组。
- 面试里先写暴力讲清楚「切段」的模型，再说明瓶颈在重复扫描，引出线段树。
