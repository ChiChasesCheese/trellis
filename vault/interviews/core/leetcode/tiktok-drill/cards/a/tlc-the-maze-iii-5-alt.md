---
id: tlc-the-maze-iii-5-alt
node: a.the-maze-iii
type: qa
step: 5
---
## Q
**LC 499 迷宫 III**｜另一种解法

距离按格数计、每走一格都是 `1`。能不能不用堆，用逐格 BFS 求出同样的答案？状态要怎么设计，什么时候选它？

## A
**思路。** 把状态细化到每一格：`(行, 列, 正在滚的方向)`，方向为 `None` 表示球停着、可以选新方向。每走一格距离加 1，图变成**无权图**，BFS 的层数就是距离。同一层里到达同一状态的多条路径只留字典序最小的；某一层第一次碰到洞时，取这一层所有进洞路径的最小值。

```python
def find_shortest_way_bfs(maze: list[list[int]], ball: list[int], hole: list[int]) -> str:
    m, n = len(maze), len(maze[0])
    dirs = (("d", 1, 0), ("l", 0, -1), ("r", 0, 1), ("u", -1, 0))
    target = (hole[0], hole[1])

    def free(r: int, c: int) -> bool:
        return 0 <= r < m and 0 <= c < n and maze[r][c] == 0

    # 状态 (行, 列, 方向)：方向为 None 表示已经停住、可以选新方向
    frontier: dict[tuple[int, int, str | None], str] = {(ball[0], ball[1], None): ""}
    visited = set(frontier)
    while frontier:
        nxt: dict[tuple[int, int, str | None], str] = {}
        found: list[str] = []
        for (r, c, d), path in frontier.items():
            for ch, dr, dc in dirs:
                if d is not None and ch != d:
                    continue                      # 正在滚的球只能继续同方向
                if not free(r + dr, c + dc):
                    continue
                nr, nc = r + dr, c + dc
                new_path = path + ch if d is None else path   # 起滚时才记下方向字母
                if (nr, nc) == target:
                    found.append(new_path)
                    continue
                key = (nr, nc, ch if free(nr + dr, nc + dc) else None)   # 前面是墙：停住
                if key not in visited and (key not in nxt or new_path < nxt[key]):
                    nxt[key] = new_path
        if found:
            return min(found)
        visited.update(nxt)
        frontier = nxt
    return "impossible"
```

运行：样例迷宫 `ball = [4,3]`：`hole = [0,1]` → `"lul"`，`hole = [3,0]` → `"impossible"`；第三个样例 → `"dldr"`。

**为什么对。** 每层恰好是距离为 `d` 的全部状态，第一次出现洞的那一层就是最短距离；同层同状态的路径之后走法相同，留字典序最小的不会丢答案（同距离的两条路径互不为前缀，接相同后缀仍保序）。

**取舍。** 逐格 BFS 状态数是 `4mn`、没有堆和 `log`，总时间 `O(mn · L)`（路径复制），思路是「拆边为单位步」，适合边权都是小整数的场合。Dijkstra 版节点少（只有停点）、代码短，是面试首选；逐格 BFS 是被要求「不用堆」时的备选。
