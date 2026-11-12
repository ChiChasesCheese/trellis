---
slug: number-of-distinct-islands-ii
---
## Q
**LC 711 不同岛屿的数量 II**｜Hard

二进制网格里四连通的 `1` 组成岛屿，形状相同或经旋转、翻转后相同算同一种。求不同形状的岛屿数。

## A
**一句话。** DFS 收集岛屿格子，对 8 种旋转翻转各自排序平移到原点，取字典序最小的当规范形放入集合去重。

```python
def canon(cells):
    forms = []
    for sx, sy, sw in product((1, -1), (1, -1), (0, 1)):
        pts = sorted((sx * (y if sw else x),
                      sy * (x if sw else y))
                     for x, y in cells)
        ox, oy = pts[0]            # 最小点平移到原点
        forms.append(tuple((x-ox, y-oy) for x, y in pts))
    return min(forms)              # 8 种形态里取最小

def num_distinct_islands2(grid):
    m, n = len(grid), len(grid[0])
    seen = [[0] * n for _ in range(m)]
    shapes = set()
    for i in range(m):
        for j in range(n):
            if grid[i][j] and not seen[i][j]:
                cells, st = [], [(i, j)]
                seen[i][j] = 1
                while st:
                    x, y = st.pop()
                    cells.append((x, y))
                    for a, b in ((x+1, y), (x-1, y),
                                 (x, y+1), (x, y-1)):
                        if (0 <= a < m and 0 <= b < n
                                and grid[a][b]
                                and not seen[a][b]):
                            seen[a][b] = 1
                            st.append((a, b))
                shapes.add(canon(cells))
    return len(shapes)
```

**复杂度。** 时间 `O(mn log mn)`，空间 `O(mn)`。

**易错点。**
- 只做 4 种旋转漏掉翻转：`L` 与 `J` 形会被数成两种。
- 变换后不平移归一化：位置不同的两个相同岛屿被数成两种。

**追问。**
- 只允许平移（LC 694）怎么改？：去掉其余 7 种变换，只做平移归一化。
- 为什么不能只用格子数当指纹？：`I` 形四格和 `L` 形四格形状不同但格子数一样。

**同模式。** LC 694 不同岛屿的数量、LC 695 岛屿的最大面积、LC 200 岛屿数量、LC 1905 统计子岛屿
