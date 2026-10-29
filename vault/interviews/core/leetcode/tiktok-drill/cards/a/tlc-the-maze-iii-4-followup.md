---
id: tlc-the-maze-iii-4-followup
node: a.the-maze-iii
type: qa
step: 4
---
## Q
**LC 499 迷宫 III**｜追问

面试官接着问：（1）如果没有洞，而是要求球**停在**终点，只返回最短距离（LC 505 迷宫 II）？（2）只问球能否停在终点（LC 490）？（3）路径可能很长，堆里存整条路径字符串太费内存，怎么办？

## A
1. **迷宫 II**：节点仍是停点，但终点必须是停点，滚动途中不截停；键只有距离，用 `best[r][c]` 记最短距离，只有更短时才入堆。

```python
import heapq
from math import inf


def shortest_distance(maze: list[list[int]], start: list[int], destination: list[int]) -> int:
    m, n = len(maze), len(maze[0])
    best = [[inf] * n for _ in range(m)]          # best[r][c]：到停点 (r, c) 的已知最短距离
    best[start[0]][start[1]] = 0
    heap = [(0, start[0], start[1])]
    while heap:
        dist, r, c = heapq.heappop(heap)
        if [r, c] == destination:
            return dist
        if dist > best[r][c]:
            continue                              # 过期条目
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc, step = r, c, 0
            while 0 <= nr + dr < m and 0 <= nc + dc < n and maze[nr + dr][nc + dc] == 0:
                nr, nc, step = nr + dr, nc + dc, step + 1
            if step and dist + step < best[nr][nc]:
                best[nr][nc] = dist + step
                heapq.heappush(heap, (dist + step, nr, nc))
    return -1
```

运行：`[[0,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,0,1,1],[0,0,0,0,0]]`，`start = [0,4]`：`destination = [4,4]` → `12`，`destination = [3,2]` → `-1`（能经过但停不下）。
2. **迷宫 I**：只问可达，边权无关，BFS 或 DFS 遍历停点，`visited` 记停点即可，`O(mn(m + n))`。
3. **省内存**：堆里只放 `(距离, 行, 列)`，另存 `parent[停点] = (上一个停点, 方向)` 回溯路径；但字典序平局需要比较完整路径，可在距离相同时临时回溯比较，或接受 `O(mn · L)` 的空间。`m, n <= 100` 时直接存字符串最简单。

**Python 提醒**：`heapq` 比较元组时逐个分量比，前面分量相等才比后面；若某个分量是不可比较的对象（如自定义节点），平局时会抛 `TypeError`，要插入一个递增计数器做第二关键字。
