---
slug: flood-fill
---
## Q
**LC 733 图像渲染**｜Easy

有一幅用 `m x n` 二维整数数组表示的图画 `image`，`image[i][j]` 是像素值。再给你三个整数 `sr`、`sc` 和 `color`。从像素 `image[sr][sc]` 开始上色填充：把它改成 `color`，再对它**上下左右四个方向**上与初始像素原来颜色相同的相邻像素做同样的事，如此重复，直到没有符合条件的像素，返回修改后的图像。`m == image.length`，`n == image[i].length`，`1 <= m, n <= 50`，`0 <= image[i][j], color < 2^16`，`0 <= sr < m`，`0 <= sc < n`。例：`image = [[1,1,1],[1,1,0],[1,0,1]]`, `sr = 1`, `sc = 1`, `color = 2` → `[[2,2,2],[2,2,0],[2,0,1]]`（右下角的 `1` 与起点不四连通，不变）；`image = [[0,0,0],[0,0,0]]`, `sr = 0`, `sc = 0`, `color = 0` → 原图不变。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 网格上的 DFS / 连通区域（connected component）遍历；改色本身当作 visited。

**一句话。** 从起点出发做 DFS，把与起点原色相同的四连通像素逐个改成新颜色，改过的像素不再等于原色，所以不会重复访问。

**识别。** 「从某点出发，把相连的同类格子都变掉」= 连通块的 DFS / BFS；`50 x 50` 允许任何线性做法。

**推导。** 无需额外 `visited`：被改成新色的像素不再等于旧色，递归遇到就停。唯一的陷阱是新色等于旧色时，改色不会改变任何像素，"已访问"标记失效，DFS 会无限循环，所以先判断 `old == color` 直接返回。

```python
def flood_fill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    old = image[sr][sc]
    if old == color:  # 新旧同色：改色不留痕迹，DFS 会在相邻格子间来回走，直接返回
        return image
    m, n = len(image), len(image[0])

    def dfs(r: int, c: int) -> None:
        if not (0 <= r < m and 0 <= c < n) or image[r][c] != old:  # 越界，或不是原色（含已改色）
            return
        image[r][c] = color  # 改色同时就是 visited 标记
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(sr, sc)
    return image
```

运行：示例 1 → `[[2,2,2],[2,2,0],[2,0,1]]`；示例 2 → 原图不变；`[[1]]`, `color = 5` → `[[5]]`。

**复杂度。** 时间 `O(m * n)`，空间 `O(m * n)`（最坏递归深度）。

**拓展优化。**
- 避免递归深度问题：用队列做 BFS，同样原地改色，改色发生在入队时（而不是出队时），避免同一格子重复入队：

```python
from collections import deque


def flood_fill_bfs(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    old = image[sr][sc]
    if old == color:
        return image
    m, n = len(image), len(image[0])
    image[sr][sc] = color
    queue = deque([(sr, sc)])
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and image[nr][nc] == old:
                image[nr][nc] = color  # 入队时就改色：之后不会再被别的格子加入
                queue.append((nr, nc))
    return image
```

**易错点。**
- 漏掉 `old == color` 的判断：示例 2（`color = 0` 且起点就是 `0`）会无限递归，`RecursionError`。
- 最坏深度：`50 x 50` 的整张图同色时，DFS 沿一条蛇形路径深入，深度可达约 `2500`，超过 CPython 默认约 `1000` 的递归上限，抛 `RecursionError`；要么 `sys.setrecursionlimit`，要么用上面的 BFS。
- 把方向写成 8 个方向（含对角线）：示例 1 的右下角 `1` 会被误改成 `2`，输出 `[[2,2,2],[2,2,0],[2,0,2]]`。

**同模式。** LC 200 岛屿数量、LC 695 岛屿的最大面积、LC 130 被围绕的区域、LC 463 岛屿的周长。
