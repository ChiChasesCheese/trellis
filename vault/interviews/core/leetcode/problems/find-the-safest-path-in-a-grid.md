---
slug: find-the-safest-path-in-a-grid
---
## Q
**LC 2812 找出最安全路径**｜Medium

`n×n` 网格（`n ≤ 400`）中 `1` 是小偷。从左上走到右下，路径的安全系数是路上格子到最近小偷曼哈顿距离的最小值，求最大安全系数。

## A
**一句话。** 先从所有小偷做多源 BFS 得每格距离，再做「最大化路径最小值」：大根堆每次扩展当前最安全的格子，第一次到终点即答案。

```python
def maximum_safeness_factor(grid):
    n = len(grid)
    dis = [[-1] * n for _ in range(n)]
    q = deque((i, j) for i in range(n) for j in range(n)
              if grid[i][j])
    for i, j in q:
        dis[i][j] = 0
    while q:                     # 多源 BFS：到最近小偷的距离
        i, j = q.popleft()
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if 0 <= x < n and 0 <= y < n and dis[x][y] < 0:
                dis[x][y] = dis[i][j] + 1
                q.append((x, y))
    h = [(-dis[0][0], 0, 0)]
    seen = {(0, 0)}
    while h:                     # 堆顶是当前能到的最安全值
        s, i, j = heappop(h)
        if i == j == n - 1:
            return -s
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if (0 <= x < n and 0 <= y < n
                    and (x, y) not in seen):
                seen.add((x, y))
                heappush(h, (max(s, -dis[x][y]), x, y))
```

**复杂度。** 时间 `O(n^2 log n)`，空间 `O(n^2)`。

**易错点。**
- 从每个格子单独 BFS 找最近小偷：`O(n^4)`，必须多源一次做完。
- 路径值取了和或最大值：安全系数是路上的最小值，压栈的值是 `min(当前值, dis)`。

**追问。**
- 不用堆？：二分答案 `t`，只走 `dis ≥ t` 的格子 BFS 看能否到终点，`O(n^2 log n)`。
- 为什么入堆就能标记？：出堆的值单调不增，先入堆的那次已是最大可能值。

**同模式。** LC 994 腐烂的橘子、LC 1631 最小体力消耗路径、LC 778 水位上升的泳池中游泳
