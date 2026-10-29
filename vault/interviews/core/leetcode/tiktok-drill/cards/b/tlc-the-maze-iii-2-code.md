---
id: tlc-the-maze-iii-2-code
node: b.the-maze-iii
type: qa
step: 2
---
## Q
**LC 499 迷宫 III**｜写出 Python 实现

`m x n`（`1 <= m, n <= 100`）的 `0/1` 迷宫，球滚到墙才停，经过洞即掉入；返回进洞的最短方向序列（`'u' 'd' 'l' 'r'`），距离为经过的空地格数，平局取字典序最小，进不了返回 `"impossible"`。

## A
**思路。** 停点为节点、滚动为边，Dijkstra。堆元素 `(距离, 路径, 行, 列)`，元组比较先比距离再比路径字典序。弹出时定型；向四个方向滚动，途中遇洞就停在洞上；洞第一次被弹出时返回路径。

```python
import heapq


def find_shortest_way(maze: list[list[int]], ball: list[int], hole: list[int]) -> str:
    m, n = len(maze), len(maze[0])
    dirs = (("d", 1, 0), ("l", 0, -1), ("r", 0, 1), ("u", -1, 0))
    target = (hole[0], hole[1])
    heap = [(0, "", ball[0], ball[1])]            # (距离, 路径, 行, 列)：元组比较 = 先比距离再比字典序
    settled: set[tuple[int, int]] = set()
    while heap:
        dist, path, r, c = heapq.heappop(heap)
        if (r, c) == target:
            return path                           # 第一个弹出的洞就是答案
        if (r, c) in settled:
            continue                              # 这个停点已经用更优的 (距离, 路径) 处理过
        settled.add((r, c))
        for ch, dr, dc in dirs:
            nr, nc, step = r, c, 0
            while 0 <= nr + dr < m and 0 <= nc + dc < n and maze[nr + dr][nc + dc] == 0:
                nr, nc, step = nr + dr, nc + dc, step + 1
                if (nr, nc) == target:            # 滚过洞口就掉进去，不再往前
                    break
            if step and (nr, nc) not in settled:
                heapq.heappush(heap, (dist + step, path + ch, nr, nc))
    return "impossible"
```

运行：样例迷宫 `ball = [4,3]`：`hole = [0,1]` → `"lul"`，`hole = [3,0]` → `"impossible"`；`[[0,0,0,0,0,0,0],[0,0,1,0,0,1,0],[0,0,0,0,1,0,0],[0,0,0,0,0,0,1]], ball = [0,4], hole = [3,5]` → `"dldr"`；`[[0,0,0]], ball = [0,0], hole = [0,1]` → `"r"`。

**复杂度。** 停点至多 `mn` 个各展开一次，每次 4 个方向各滚 `O(m + n)`：`O(mn(m + n))`；另有 `O(mn)` 次堆操作，每次 `O(log(mn))` 次路径字符串比较。空间 `O(mn · L)`，`L` 是路径长度。

**写法要点。** 把路径放进元组第二位，`heapq` 的元组比较就完成了「距离优先、字典序其次」，不用写比较函数；行列放在后面只是载荷，距离和路径都相同时才会比到它们，整数可比较不会报错；`step` 为 `0` 表示这个方向一出发就是墙，不产生边；`settled` 在弹出时更新（惰性删除），堆里同一停点的旧条目弹出后直接跳过。
