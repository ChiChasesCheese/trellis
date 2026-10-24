---
id: tlc-shortest-distance-from-all-buildings-4-followup
node: b.shortest-distance-from-all-buildings
type: qa
step: 4
---
## Q
**LC 317 离建筑物最近的距离**｜追问

面试官接着问：（1）不仅要最短总距离，还要给出具体建在哪一格？（2）没有障碍、只有建筑，能不能不用 BFS？（3）怎样提前发现无解，少做无用的 BFS？

## A
1. **返回位置**：最后的 `min` 改成对 `(总距离, 行, 列)` 取最小；`total`、`reach` 是主解法里累加出来的两张表。
```python
def best_spot(grid: list[list[int]], total: list[list[int]], reach: list[list[int]],
              buildings: int) -> tuple[int, int, int] | None:
    m, n = len(grid), len(grid[0])
    return min(((total[r][c], r, c) for r in range(m) for c in range(n)
                if grid[r][c] == 0 and reach[r][c] == buildings), default=None)
```
元组比较先比距离，再比坐标；`best is None` 表示无解。
2. **没有障碍和建筑阻挡**：每步都能走，距离就是曼哈顿距离，行和列互相独立，最优点的行取所有建筑行坐标的中位数，列同理（LC 296），`O(B log B)`，不需要 BFS。有了障碍或建筑阻挡，曼哈顿距离不再成立，只能 BFS。
3. **提前剪枝**：第一幢建筑 BFS 之后，没被它访问到的空地以后都不可能合格。可以直接用「被所有建筑访问过」的格子集合逐幢求交，一旦交集为空立即返回 `-1`；或者在某幢建筑 BFS 时发现它到不了任何空地（四周被封死）就直接返回 `-1`。

**Python 提醒**：`min(generator, default=...)` 的 `default` 只在生成器为空时生效；如果生成器里是元组，比较会先比第一个元素，相同才比后面的，这正是想要的「距离相同取靠前坐标」。
