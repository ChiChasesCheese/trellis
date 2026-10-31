---
id: tlc-number-of-islands-ii-0-whole
node: c.number-of-islands-ii
type: qa
---
## Q
**LC 305 岛屿数量 II**｜Hard · LC TikTok 全时段热度 38/100

`m x n` 的二维网格初始全是水（`0`）。给定 `positions`，第 `i` 次操作 `positions[i] = [ri, ci]` 把该位置的水变成陆地。返回数组 `answer`，`answer[i]` 是第 `i` 次操作之后岛屿的数量；岛屿是上下左右相邻的陆地连成的块。`1 <= m, n, positions.length <= 10^4`，`1 <= m * n <= 10^4`，`0 <= ri < m`，`0 <= ci < n`。进阶：能否做到 `O(k log(mn))`，`k = positions.length`。例：`m = 3, n = 3, positions = [[0,0],[0,1],[1,2],[2,1]]` → `[1, 1, 2, 3]`；`m = 1, n = 1, positions = [[0,0]]` → `[1]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 并查集（Union-Find）：每加一块陆地先计数 `+1`，再与上下左右已有的陆地合并，每次成功合并计数 `-1`。

**识别。** 「只增不减的连通性，要求每步之后的连通块数」：并查集的标准场景（动态连通性）。重新扫描整张图是 `O(k · m · n)`，被「进阶」排除。

**推导。** 每加一块陆地 `x`，新岛屿数 = 旧数 + 1 - 与 `x` 相邻的、此前互不连通的岛屿个数。判断「是否本来已连通」正好是 `find` 要回答的。并查集只对陆地建立，水格不入集合。

```python
def num_islands2(m: int, n: int, positions: list[list[int]]) -> list[int]:
    parent: dict[int, int] = {}                  # 只有陆地在这里；格子编号 = r * n + c

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]        # 路径折半，均摊近似 O(1)
            x = parent[x]
        return x

    ans: list[int] = []
    islands = 0
    for r, c in positions:
        cell = r * n + c
        if cell not in parent:                   # 重复加陆地：什么都不变
            parent[cell] = cell
            islands += 1                         # 先当作一座新岛
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                nxt = nr * n + nc
                if 0 <= nr < m and 0 <= nc < n and nxt in parent:
                    root_a, root_b = find(cell), find(nxt)
                    if root_a != root_b:         # 之前不连通：合并，岛屿少一座
                        parent[root_a] = root_b
                        islands -= 1
        ans.append(islands)
    return ans
```

运行：`(3, 3, [[0,0],[0,1],[1,2],[2,1]])` → `[1, 1, 2, 3]`，`(1, 1, [[0,0]])` → `[1]`；`(1, 3, [[0,0],[0,2],[0,1]])` → `[1, 2, 1]`（最后一块把两座岛连成一座）；`(1, 2, [[0,0],[0,0]])` → `[1, 1]`（重复位置）。

**复杂度。** 时间 `O(k · α(mn))`，近似 `O(k)`，满足进阶；空间 `O(min(k, mn))`。

**拓展优化。**
- 再加按大小合并（union by size）可得到严格的反阿克曼上界；这里路径折半已足够。
- 同时要最大岛面积：根节点上维护 `size`，合并时相加并更新全局最大值，其余不变。
- 陆地也可以变回水：并查集不支持删除，需要离线反向处理（把时间倒过来，删变成加）。

**易错点。**
- 重复位置当作新陆地：`islands` 多加一次。`positions` 里允许出现重复，已是陆地的位置要直接跳过。
- 只和已有陆地合并这一条件漏了：`nxt in parent` 缺失会对水格 `find`，抛 `KeyError`。
- `islands -= 1` 写在 `find` 之前或不判断根是否相同：同一座岛从两个方向相邻时会被减两次。

**追问。**
- 为什么用字典而不是 `list(range(m * n))`：初始全是水，陆地稀疏时按需建立更省，`m * n` 很大时尤其明显。
- 网格是环面（左右、上下首尾相接）：邻居坐标取模，其余不变。

**同模式。** LC 200 岛屿数量、LC 547 省份数量、LC 684 冗余连接、LC 721 账户合并、LC 695 岛屿的最大面积。
