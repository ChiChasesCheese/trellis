---
id: tlc-number-of-distinct-islands-ii-5-alt
node: b.number-of-distinct-islands-ii
type: qa
step: 5
---
## Q
**LC 711 不同岛屿的数量 II**｜另一种解法

不取「8 个形态的最小者」，还有什么办法对岛屿去重（`m x n <= 50 x 50`，形状含旋转、翻转）？它与规范形取最小相比，什么时候该选哪个？

## A
**把 8 个形态全部记进「已见」集合。** 对每个新岛，算出它的 8 个归一化形态；如果第一个形态已经在 `known` 里，说明同类岛已出现过；否则计数加一，并把这 8 个形态都加入 `known`：

```python
from itertools import product


def all_forms(cells: list[tuple[int, int]]) -> list[tuple[tuple[int, int], ...]]:
    forms = []
    for sx, sy, swap in product((1, -1), (1, -1), (False, True)):
        pts = sorted((sx * (y if swap else x), sy * (x if swap else y)) for x, y in cells)
        ox, oy = pts[0]
        forms.append(tuple((x - ox, y - oy) for x, y in pts))
    return forms


def num_distinct_islands2_alt(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    seen = [[False] * n for _ in range(m)]
    known: set[tuple[tuple[int, int], ...]] = set()     # 已见岛屿的全部 8 个形态
    count = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] and not seen[i][j]:
                cells: list[tuple[int, int]] = []
                seen[i][j] = True
                stack = [(i, j)]
                while stack:
                    x, y = stack.pop()
                    cells.append((x, y))
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] and not seen[nx][ny]:
                            seen[nx][ny] = True
                            stack.append((nx, ny))
                forms = all_forms(cells)
                if forms[0] not in known:
                    count += 1
                    known.update(forms)
    return count
```

`50 x 50` 全 `1` 返回 `1`，两个示例都是 `1`，和规范形取最小的版本结果一致。

**怎么选。**
- 取最小者：每类只存 `1` 个键，可直接用 `Counter` 统计每类个数，是首选写法。
- 全部形态入集合：不需要比较大小，逻辑最直观，但每类多存 `8` 个键；适合只要「是否见过」的场景。
- 旋转翻转不变量（如全部点对距离平方的多重集）可当预过滤，它是必要条件而不是充分条件：一般点集上存在不同形状、距离多重集却相同的例子，所以过滤之后仍要用精确的形态比较，不能直接拿它当答案。
