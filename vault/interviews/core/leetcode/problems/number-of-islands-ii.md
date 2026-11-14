---
slug: number-of-islands-ii
---
## Q
**LC 305 岛屿数量 II**｜Hard

`m x n` 网格初始全是水。依次把 `positions` 中的位置变成陆地，返回每次操作后的岛屿数量。

## A
**一句话。** 并查集：加一块陆地先计数加一，再与四周已有的陆地合并，每次成功合并计数减一。

```python
def num_islands2(m, n, positions):
    parent = {}              # 只存陆地，编号 r * n + c

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # 路径折半
            x = parent[x]
        return x

    ans, islands = [], 0
    for r, c in positions:
        cell = r * n + c
        if cell not in parent:       # 重复位置什么都不变
            parent[cell] = cell
            islands += 1
            for dx, dy in (1, 0), (-1, 0), (0, 1), (0, -1):
                x, y = r + dx, c + dy
                nxt = x * n + y
                if (0 <= x < m and 0 <= y < n
                        and nxt in parent):
                    a, b = find(cell), find(nxt)
                    if a != b:       # 之前不连通：合并
                        parent[a] = b
                        islands -= 1
        ans.append(islands)
    return ans
```

**复杂度。** 时间 `O(k·α(mn))`，空间 `O(k)`。

**易错点。**
- 重复位置当作新陆地：`islands` 多加一次，已是陆地的位置要直接跳过。
- 漏了 `nxt in parent`：对水格 `find` 抛 `KeyError`。
- 不比较根就 `islands -= 1`：同一座岛从两个方向相邻时被减两次。

**追问。**
- 为什么用字典？：陆地稀疏时按需建立，比 `list(range(mn))` 省空间。
- 还想支持把陆地变回水？：并查集不支持删除，只能离线反向处理或重建。
- 网格按行流式到达、存不下整张图？：仍用并查集，只留上一行的标签，不再出现在新一行的块当场结算并删掉，内存 `O(列数)`。

**同模式。** LC 200 岛屿数量、LC 547 省份数量、LC 684 冗余连接、LC 721 账户合并
