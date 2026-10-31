---
id: tlc-block-placement-queries-0-whole
node: p4.block-placement-queries
type: qa
---
## Q
**LC 3161 物块放置查询**｜Hard · LC TikTok 热度 88/100（近 3 个月）

数轴从原点 `0` 起沿正方向无限延伸。给二维数组 `queries`，有两种操作：`[1, x]`：在距离原点 `x` 处建一个障碍物（保证此时 `x` 处没有障碍物）；`[2, x, sz]`：判断能否在 `[0, x]` 范围内**完整**放下一个长度为 `sz` 的物块，物块不能与任何障碍物重合，但可以恰好接触；只是询问，不真的放置，查询之间互相独立。按顺序返回每个 `[2, ...]` 操作的布尔结果。`1 <= queries.length <= 15 * 10^4`，`2 <= queries[i].length <= 3`，`1 <= x, sz <= min(5 * 10^4, 3 * queries.length)`，至少有一个类型 2 操作。例：`[[1,2],[2,3,3],[2,3,1],[2,2,2]]` → `[false,true,true]`；`[[1,7],[2,7,6],[1,2],[2,7,5],[2,7,6]]` → `[true,true,false]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 障碍物把数轴切成若干空隙。把原点也当作障碍物，每个障碍物 `p` 对应一个「左空隙」`p - 前一个障碍物`；用线段树（区间最大值）按坐标存这些空隙。插入障碍物 `x` 只改两个位置：`x` 自己（新建）和它的后继（空隙变小）。查询时找到 `x` 左边最近的障碍物 `p`，答案是 `max(线段树 [0, p] 的最大值, x - p) >= sz`。`O(q log M)`。

**识别。** 修改和查询交替出现 → 数据结构题。要维护「前缀里的最大空隙」→ 区间最大值的线段树（或树状数组）；要找 `x` 左右最近的障碍物 → 有序集合的前驱 / 后继。坐标不超过 `5 * 10^4`，可以直接当线段树的下标，不用离散化。Python 没有内置有序集合，用有序列表加 `bisect`。

**推导。** 暴力：每个查询扫描 `[0, x]` 里的全部障碍物，找最大空隙，`O(q · k)`，最坏 `1.5 * 10^5 × 5 * 10^4 ≈ 7.5 * 10^9`，太慢。观察一：空隙只取决于相邻两个障碍物，插入 `x` 只把一个空隙拆成两个，所以只有两个数变化。观察二：查询只看 `[0, x]`；`x` 左边的完整空隙（两端都是障碍物）不受 `x` 影响，只有最后一段 `[p, x]` 被 `x` 截短，要单独算 `x - p`。于是把「完整空隙」按右端点 `p` 存进线段树，查询就是一个前缀最大值，再和尾段取最大。

```python
from bisect import bisect_left, bisect_right


def get_results(queries: list[list[int]]) -> list[bool]:
    size = max(q[1] for q in queries) + 1
    tree = [0] * (2 * size)             # 迭代线段树（区间最大值）：叶子 x = 以障碍物 x 结尾的空隙长度

    def update(pos: int, val: int) -> None:
        pos += size
        tree[pos] = val
        while pos > 1:
            pos >>= 1
            tree[pos] = max(tree[2 * pos], tree[2 * pos + 1])

    def query_max(r: int) -> int:       # 下标 [0, r] 上的最大值
        res, lo, hi = 0, size, r + 1 + size
        while lo < hi:
            if lo & 1:
                res = max(res, tree[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                res = max(res, tree[hi])
            lo >>= 1
            hi >>= 1
        return res

    obstacles = [0]                     # 有序的障碍物位置；原点当作哨兵
    ans: list[bool] = []
    for op, x, *rest in queries:
        if op == 1:
            k = bisect_left(obstacles, x)               # obstacles[k-1] 是前驱，obstacles[k] 是后继
            update(x, x - obstacles[k - 1])             # x 左边的空隙：x 到前驱
            if k < len(obstacles):                      # 后继的空隙被 x 截短
                update(obstacles[k], obstacles[k] - x)
            obstacles.insert(k, x)
        else:
            p = obstacles[bisect_right(obstacles, x) - 1]   # [0, x] 内最右的障碍物
            ans.append(max(query_max(p), x - p) >= rest[0])  # 之前的最大空隙，或最后一段 [p, x]
    return ans
```

运行：`[[1,2],[2,3,3],[2,3,1],[2,2,2]]` → `[False, True, True]`，`[[1,7],[2,7,6],[1,2],[2,7,5],[2,7,6]]` → `[True, True, False]`，`1.5 * 10^5` 条、坐标到 `5 * 10^4` 的随机输入也能很快跑完。

**复杂度。** 时间 `O(q log M)`，`M` 是最大坐标（至多 `5 * 10^4`）；`list.insert` 的搬移最多 `5 * 10^4` 个元素，是极快的内存拷贝，实际可忽略。空间 `O(M)`。

**易错点。**
- 漏掉最后一段 `[p, x]`：只比较障碍物之间的完整空隙。`[[1,2],[2,5,3]]` 会得到 `False`，正确是 `True`（`[2,5]` 长 `3`）。
- 插入后不更新后继的空隙：`[[1,7],[2,7,6],[1,2],[2,7,5],[2,7,6]]` 里 `7` 的空隙应从 `7` 缩成 `5`，不更新会得到 `[True, True, True]`，正确是 `[True, True, False]`。
- 不放原点哨兵：第一个障碍物插入时 `obstacles[k - 1]` 对空列表抛 `IndexError`；列表非空而新障碍物最靠左时，`k - 1 = -1` 悄悄取到最右边的元素，空隙变成负数。
- 边界：物块可以恰好接触障碍物，所以是 `>= sz`，不是 `> sz`。

**追问。**
- 离线倒序处理：先把所有障碍物都放上，倒着回放操作，「建障碍物」变成「删障碍物」，空隙只会变大，于是线段树可以换成只做「取大更新」的树状数组，前驱用并查集找，常数更小。
- 坐标很大（如 `10^9`）：先离线收集所有 `x`，离散化后再建树。
- 还要支持删除障碍物：线段树同样能改回更大的空隙，找前驱后继的有序集合也要支持删除。

**同模式。** LC 307 区域和检索——数组可修改、LC 315 计算右侧小于当前元素的个数（树状数组）、LC 218 天际线问题、LC 729 我的日程安排表 I、LC 699 掉落的方块。
