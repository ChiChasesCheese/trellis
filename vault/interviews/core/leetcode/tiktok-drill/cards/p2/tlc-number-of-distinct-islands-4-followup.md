---
id: tlc-number-of-distinct-islands-4-followup
node: p2.number-of-distinct-islands
type: qa
step: 4
---
## Q
**LC 694 不同岛屿的数量**｜追问

面试官接着问：（1）旋转和翻转后重合也算同一种形状（LC 711），签名怎么改？（2）为什么不直接用 DFS 的访问顺序当签名？（3）网格很大时内存怎么控制？

## A
1. **旋转加翻转**：同一座岛有 8 种姿态（4 次旋转，各有镜像）。对每种姿态：用坐标变换生成格子，排序后以第一个格子为原点平移归一，得到一个元组；取 8 个元组里字典序最小的当签名。

```python
def num_distinct_islands_ii(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    seen: set[tuple[int, int]] = set()
    shapes: set[tuple[tuple[int, int], ...]] = set()
    transforms = [lambda x, y: (x, y), lambda x, y: (x, -y), lambda x, y: (-x, y), lambda x, y: (-x, -y),
                  lambda x, y: (y, x), lambda x, y: (y, -x), lambda x, y: (-y, x), lambda x, y: (-y, -x)]
    for r0 in range(rows):
        for c0 in range(cols):
            if grid[r0][c0] != 1 or (r0, c0) in seen:
                continue
            stack, cells = [(r0, c0)], []
            seen.add((r0, c0))
            while stack:
                r, c = stack.pop()
                cells.append((r, c))
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1 and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            forms = []
            for t in transforms:
                moved = sorted(t(r, c) for r, c in cells)
                mr, mc = moved[0]
                forms.append(tuple((r - mr, c - mc) for r, c in moved))
            shapes.add(min(forms))
    return len(shapes)
```

`[[1,1,0,0,0],[1,0,0,0,0],[0,0,0,0,1],[0,0,0,1,1]]` 里两座 L 形互为旋转 → `1`，而 LC 694 的平移规则会把它们算成 `2`。
2. **访问顺序当签名**：可以，但要在回溯时记录"退出"标记（比如每次递归返回追加 `0`），否则不同形状可能走出同样的方向序列。偏移集合的做法不需要这个细节，更不容易写错。
3. **内存**：签名大小与岛屿格数成正比，总量不超过 `O(mn)`。如果只要数量、岛很大，可以把签名换成它的哈希值，代价是极小概率的碰撞。

**Python 提醒**：`list` 不可哈希，不能直接放进 `set`；签名要转成 `tuple` 或 `frozenset`。元组要先排序，否则同一形状遍历顺序不同会得到不同的元组。
