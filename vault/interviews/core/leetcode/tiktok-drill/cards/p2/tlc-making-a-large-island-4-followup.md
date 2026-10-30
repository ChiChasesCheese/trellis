---
id: tlc-making-a-large-island-4-followup
node: p2.making-a-large-island
type: qa
step: 4
---
## Q
**LC 827 最大人工岛**｜追问

面试官接着问：（1）要返回应该翻哪一格？（2）网格会动态更新（一格一格变成 `1`），要随时回答最大岛面积？（3）网格很大，放不进内存怎么办？（4）`500×500` 全 `1` 让递归 DFS 爆栈怎么办？

## A
1. **返回位置**：枚举 `0` 时用 `if value > best: best, pos = value, (i, j)` 同时记坐标。若没有 `0` 可翻，则返回「不用翻」，约定好返回值（如 `None`）。
2. **动态加点**（类似 LC 305 岛屿数量 II）：用并查集。每新增一个 `1`，先自成一个集合（`size = 1`），再与四邻中已是 `1` 的格子合并，同时用一个变量维护全局最大面积，每次合并后 `max` 一下，均摊近似 `O(1)`。DFS 版本无法增量维护，只能重算。
3. **超大网格**：逐行流式处理，维护上一行的并查集标号，只需 `O(n)` 的状态——这和「图像的连通域标记」（two-pass connected-component labeling）是同一套路：第一遍给临时标号并记录等价关系，第二遍把等价的标号合并。需要 `0` 的翻转答案时，还要保留每个 `0` 邻接的岛信息，或二次扫描。
4. **递归爆栈**：`dfs` 深度可达 `2.5×10^5`，超过默认上限约 `1000`。把标号换成显式栈版 `flood`：
```python
def flood(grid: list[list[int]], label: list[list[int]], i: int, j: int, tag: int) -> int:
    """显式栈版：给 (i, j) 所在的岛打上 tag，返回面积；用来替换递归的 dfs。"""
    n = len(grid)
    label[i][j] = tag
    stack, area = [(i, j)], 0
    while stack:
        x, y = stack.pop()
        area += 1
        for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= a < n and 0 <= b < n and grid[a][b] == 1 and label[a][b] == 0:
                label[a][b] = tag
                stack.append((a, b))
    return area
```
   调用处写 `size[tag] = flood(grid, label, i, j, tag)` 即可；也可以 `sys.setrecursionlimit` 调大。

**Python 提醒**：`{label[a][b] for a, b in neighbors(i, j)}` 里 `neighbors` 是生成器，每次调用都新建一个，可以放心重复使用；如果把生成器对象存起来遍历第二次，它已经耗尽，什么都不会产出。另外 `sum(dfs(...) for ...)` 这种生成器写法会在深递归里耗尽 C 栈，深递归里用普通 `for` 循环累加。
