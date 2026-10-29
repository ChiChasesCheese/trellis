---
id: tlc-pacific-atlantic-water-flow-4-followup
node: a.pacific-atlantic-water-flow
type: qa
step: 4
---
## Q
**LC 417 太平洋大西洋水流问题**｜追问

面试官接着问：（1）只要满足条件的格子个数？（2）一共有 `k` 个海洋（任意边界段）？（3）为什么不用递归 DFS，或者用 DFS 要注意什么？

## A
1. **只要个数**：`len(pacific & atlantic)`，不需要构造列表，也不需要排序，时间仍是 `O(mn)`。
2. **`k` 个海洋**：对每个海洋各做一次 `flood`，结果集合逐个相交。
```python
from functools import reduce

def reach_all(sets: list[set[tuple[int, int]]]) -> set[tuple[int, int]]:
    return reduce(set.intersection, sets)
```
`reach_all([{(0, 0), (1, 1)}, {(1, 1), (2, 2)}])` → `{(1, 1)}`。总时间 `O(k · mn)`；如果每个格子只关心「能到几个海洋」，也可以用一个计数矩阵累加，空间 `O(mn)`。
3. **递归 DFS**：在 `200 × 200` 的一路上坡（比如 `h[r][c] = r + c`）上，一次 DFS 的递归深度可达格子数 `4 · 10^4`，远超默认的 `1000`，会 `RecursionError`；BFS 或显式栈没有这个问题。面试里先说清楚这一点，再写 BFS。

**Python 提醒**：`set.intersection` 可以接收多个参数，`reduce(set.intersection, sets)` 等价于 `sets[0] & sets[1] & ...`；对空列表调用 `reduce` 会抛 `TypeError`，海洋个数至少为一时才安全。
