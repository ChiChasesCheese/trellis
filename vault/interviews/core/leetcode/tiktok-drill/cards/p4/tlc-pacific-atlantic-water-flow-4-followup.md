---
id: tlc-pacific-atlantic-water-flow-4-followup
node: p4.pacific-atlantic-water-flow
type: qa
step: 4
---
## Q
**LC 417 太平洋大西洋水流问题**｜追问

面试官接着问：（1）网格全是同一高度，递归 DFS 会怎样，怎么改成 BFS？（2）只要满足条件的格子个数？（3）一共有 `k` 个海洋（任意边界段）？

## A
1. **深搜与 BFS**：`200 × 200` 全是同一高度时，从边界出发一次 DFS 能深入上万格，递归深度远超 CPython 默认的 `1000`，会抛 `RecursionError`；可以 `sys.setrecursionlimit` 调高，或改成多源 BFS，用 `deque` 逐层扩展，没有递归：
```python
from collections import deque


def pacific_atlantic_bfs(heights: list[list[int]]) -> list[list[int]]:
    m, n = len(heights), len(heights[0])

    def flood(starts: list[tuple[int, int]]) -> set[tuple[int, int]]:
        seen = set(starts)                     # 从海洋出发，逆流而上：只走向不矮于当前格的邻居
        queue = deque(starts)
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen and heights[nr][nc] >= heights[r][c]:
                    seen.add((nr, nc))
                    queue.append((nr, nc))
        return seen

    pacific = flood([(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)])
    atlantic = flood([(m - 1, c) for c in range(n)] + [(r, n - 1) for r in range(m - 1)])
    return [[r, c] for r, c in sorted(pacific & atlantic)]
```
2. **只要个数**：`len(pacific & atlantic)`，不需要构造列表，也不需要排序，时间仍是 `O(mn)`。
3. **`k` 个海洋**：对每个海洋各做一次 `reach`，结果集合逐个相交。
```python
from functools import reduce

def reach_all(sets: list[set[tuple[int, int]]]) -> set[tuple[int, int]]:
    return reduce(set.intersection, sets)
```
`reach_all([{(0, 0), (1, 1)}, {(1, 1), (2, 2)}])` → `{(1, 1)}`。总时间 `O(k · mn)`；如果每个格子只关心「能到几个海洋」，也可以用一个计数矩阵累加，空间 `O(mn)`。

**Python 提醒**：`set.intersection` 可以接收多个参数，`reduce(set.intersection, sets)` 等价于 `sets[0] & sets[1] & ...`；对空列表调用 `reduce` 会抛 `TypeError`，海洋个数至少为一时才安全。
