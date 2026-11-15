---
slug: maximum-partition-factor
---
## Q
**LC 3710 最大划分因子**｜Hard

平面上 `n <= 500` 个点，分成恰好两个非空组。划分因子 = 同组点对的最小曼哈顿距离（`n = 2` 时为 0）。求最大划分因子。

## A
**一句话。** 因子 `>= D` 等价于「距离 `< D` 的点对都分在两组」，即这些边构成二分图；按距离从小到大加边、用奇偶并查集维护「必须异组」，第一条造成奇环的边的距离就是答案。

```python
def max_partition_factor(points):
    n = len(points)
    if n == 2:
        return 0
    edges = sorted(
        (abs(x1 - x2) + abs(y1 - y2), i, j)
        for i, (x1, y1) in enumerate(points)
        for j, (x2, y2) in enumerate(points[:i]))
    parent = list(range(n))
    parity = [0] * n           # 与父结点是否异组

    def find(x):
        if parent[x] != x:
            p = parent[x]
            parent[x] = find(p)
            parity[x] ^= parity[p]   # 压缩后：与根是否异组
        return parent[x]

    for d, i, j in edges:      # 由近到远，要求 i、j 异组
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
            parity[ri] = parity[i] ^ parity[j] ^ 1
        elif parity[i] == parity[j]:
            return d           # 奇环：这一对只能同组
    return 0
```

**复杂度。** 时间 `O(n² log n)`，空间 `O(n²)`。

**易错点。**
- 并入时把 `parity[ri]` 设成 1：要按 `i`、`j` 各自到根的奇偶算，`parity[i] ^ parity[j] ^ 1`。
- 冲突时返回前一条边的距离：距离 `< d` 的边都能异组，因子恰好能达到 `d`。

**追问。**
- 二分写法？：二分 `D`，对距离 `< D` 的边做 BFS 染色判二分图，`O(n² log U)`，思路更直接。
- 为什么两组一定非空？：`n >= 3` 时只要有边，二分图两侧都非空；若一条边都没加就冲突不了，不会走到那里。

**同模式。** LC 684 冗余连接、LC 886 可能的二分法、LC 1631 最小体力消耗路径
