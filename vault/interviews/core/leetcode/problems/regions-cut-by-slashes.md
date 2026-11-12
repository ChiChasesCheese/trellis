---
slug: regions-cut-by-slashes
---
## Q
**LC 959 由斜杠划分区域**｜Medium

`n x n` 网格每格是 `/`、`\` 或空格，斜杠把格子切开，返回被分出的区域数。

## A
**一句话。** 每格按对角线拆成上右下左 4 个三角形当结点，并查集按斜杠和相邻关系合并，剩下的集合数就是答案。

```python
def regions_by_slashes(grid):
    n = len(grid)
    parent = list(range(4 * n * n))   # 每格 4 块：0上 1右 2下 3左
    regions = 4 * n * n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        nonlocal regions
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            regions -= 1
    for r in range(n):
        for c in range(n):
            t = (r * n + c) * 4
            rt, b, lf = t + 1, t + 2, t + 3
            ch = grid[r][c]
            if ch == "/":
                union(t, lf)
                union(b, rt)
            elif ch == "\\":
                union(t, rt)
                union(b, lf)
            else:
                union(t, rt)
                union(rt, b)
                union(b, lf)
            if r + 1 < n:            # 下三角接下方的上三角
                union(b, ((r + 1) * n + c) * 4)
            if c + 1 < n:            # 右三角接右边的左三角
                union(rt, (r * n + c + 1) * 4 + 3)
    return regions
```

**复杂度。** 时间 `O(n²·α)`，空间 `O(n²)`。

**易错点。**
- 一格当一个结点：`["/"]` 得 `1`，应为 `2`。
- 跨格连错方位：必须下接上、右接左。
- 反斜杠写成 `"\"`：语法错误，要写 `"\\"`。

**追问。**
- 要每个区域的面积？：三角形按根分组计数，每块占 1/4 格。
- 还有别的做法吗？：把每格放大成 `3x3` 点阵画线，数连通块（DFS）。

**同模式。** LC 200 岛屿数量、LC 547 省份数量、LC 130 被围绕的区域、LC 765 情侣牵手
