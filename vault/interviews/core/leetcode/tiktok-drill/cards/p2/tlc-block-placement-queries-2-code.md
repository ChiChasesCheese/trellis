---
id: tlc-block-placement-queries-2-code
node: p2.block-placement-queries
type: qa
step: 2
---
## Q
**LC 3161 物块放置查询**｜写出 Python 实现

数轴上的操作序列 `queries`（至多 `15 * 10^4` 条）：`[1, x]` 在 `x` 处建障碍物；`[2, x, sz]` 询问能否在 `[0, x]` 内完整放下长度为 `sz` 的物块（可以恰好接触障碍物）。坐标和长度不超过 `min(5 * 10^4, 3 * queries.length)`。返回每个类型 2 操作的结果。用线段树加有序列表实现。

## A
**思路。** 把原点当作障碍物，每个障碍物位置 `p` 在线段树里存「`p` 与前一个障碍物的距离」。插入 `x`：用 `bisect_left` 找到前驱和后继，写入 `x` 的值，并把后继的值改小。查询：用 `bisect_right` 找 `x` 左边最近的障碍物 `p`，取线段树 `[0, p]` 的最大值与尾段 `x - p` 的较大者，和 `sz` 比较。

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

**复杂度。** 时间 `O(q log M)`：线段树单点更新和前缀查询各 `O(log M)`；`list.insert` 搬移至多 `5 * 10^4` 个元素；空间 `O(M)`。

**写法要点。** 迭代（自底向上）线段树只要一个长度 `2 * size` 的列表，叶子在 `size + i`，对满足交换律的 `max` 不要求 `size` 是 2 的幂，比递归线段树短、也快；`query_max` 用半开区间 `[lo, hi)`，奇数端点就是「不能被父节点整体覆盖」的叶子；`for op, x, *rest in queries` 用星号解包，类型 1 的操作 `rest` 为空，类型 2 时 `rest[0]` 是 `sz`；`bisect_left` 找前驱 / 后继位置，`bisect_right` 找 `<= x` 的最后一个障碍物；`update` 和 `query_max` 是闭包，直接读写外层的 `tree` 和 `size`。
