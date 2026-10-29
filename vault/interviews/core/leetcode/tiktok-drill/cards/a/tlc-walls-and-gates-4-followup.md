---
id: tlc-walls-and-gates-4-followup
node: a.walls-and-gates
type: qa
step: 4
---
## Q
**LC 286 墙与门**｜追问

面试官接着问：（1）不仅要距离，还要知道最近的是哪扇门？（2）不同格子走过去的代价不同（有泥地、有草地）？（3）不允许修改输入，要返回新网格？

## A
1. **记录最近的门**：队列元素多带一个门的编号，扩散时继承。
```python
from collections import deque

def nearest_gate_id(rooms: list[list[int]]) -> list[list[int]]:
    m, n = len(rooms), len(rooms[0])
    owner = [[-1] * n for _ in range(m)]                # 每格最近门的编号，-1 表示没有
    queue: deque[tuple[int, int]] = deque()
    for r in range(m):
        for c in range(n):
            if rooms[r][c] == 0:
                owner[r][c] = len(queue)                # 按入队顺序给门编号
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and rooms[nr][nc] > 0 and owner[nr][nc] == -1:
                owner[nr][nc] = owner[r][c]
                queue.append((nr, nc))
    return owner
```
`[[0,INF,INF,INF,0]]` → `[[0,0,0,1,1]]`（下标 `2` 到两扇门等距，先到的门获胜）。
2. **代价不同**：BFS 的「先到即最短」不再成立，改 Dijkstra：`heapq` 里放 `(距离, r, c)`，弹出时若距离比已记录的大就跳过；多源时把所有门以距离 `0` 一起压入。
3. **不改输入**：先 `dist = [row[:] for row in rooms]`，在拷贝上做同样的 BFS。不要写 `[row] * m` 或 `rooms.copy()`，它们让内外层列表共享引用，改拷贝会改到原网格。

**Python 提醒**：`[[INF] * n] * m` 得到 `m` 个指向同一行的引用，改一格全部跟着变；二维数组要写 `[[INF] * n for _ in range(m)]`。
