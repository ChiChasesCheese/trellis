---
id: tlc-xun-bao-0-whole
node: b.xun-bao
type: qa
---
## Q
**LCP 13 寻宝**｜Hard · CodeTop 国内累计 2 次 · 最近 2026-08-01（CodeTop）

迷宫是一个用字符串数组表示的二维矩阵：`S` 是唯一的入口，`T` 是唯一的宝藏。宝藏被若干机关 `M` 保护，**所有机关都被触发**才能拿到宝藏。触发机关要把一块重石放在它上面；迷宫里有若干石堆 `O`，每个石堆有无限块重石，但每次**只能搬一块**。`#` 是墙，不能走入；`.` 可随意通行；石堆、机关、起点、终点都可以通行。每步向上 / 下 / 左 / 右移动一格，不能移出迷宫；搬起和放下石头不算步数。求从起点出发，最后拿到宝藏所需的最少步数，无法拿到则返回 `-1`。`1 <= maze.length <= 100`，`1 <= maze[i].length <= 100`，各行等长；`S` 和 `T` 各恰有一个；`0 <= M 的数量 <= 16`；`0 <= O 的数量 <= 40`，有 `M` 时保证至少有一个 `O`。例：`["S#O","M..","M.T"]` → `16`；`["S#O","M.#","M.T"]` → `-1`；`["S#O","M.T","M.."]` → `17`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先用 BFS 求出需要的最短距离，把「从机关 `i` 出发，去某个石堆搬一块石头，再放到机关 `j`」压缩成机关之间的边权 `hop[i][j] = min(石堆) 距离(i, 石堆) + 距离(石堆, j)`；再对至多 `16` 个机关做**状态压缩 DP**（旅行商问题 TSP）：`dp[mask][j]` 是已触发集合为 `mask`、人站在机关 `j` 上的最少步数；最后加上机关 `j` 到宝藏的距离。

**识别。** 「至多 `16` 个必须全部访问的点 + 最短总路程」是状态压缩 DP（TSP）的信号。迷宫里两点的最短路是 BFS。直接在 `(行, 列, 已触发集合, 是否搬着石头)` 上搜索，状态数约 `10^4 * 2^16 * 2 ≈ 1.3 * 10^9`，太大；必须先把迷宫压缩成「关键点之间的距离」。

**推导。** 暴力：在完整状态上做 Dijkstra，小迷宫可以，大迷宫不行。洞察一：搬石头的动作永远是「走到某个石堆 → 走到某个机关」，中间任何停留都没有价值，所以只有 `S`、`T`、`M`、`O` 这些关键点重要，其余只提供距离。洞察二：每个机关的触发都是「去石堆拿 → 送到机关」的一次往返，而石堆无限、与其他机关的状态无关，所以从机关 `i` 到机关 `j` 的最优代价 `hop[i][j]` 可以独立预计算，起点同理：`first[j] = min(石堆) 距离(S, 石堆) + 距离(石堆, j)`。洞察三：触发顺序就是机关的一个排列，用 TSP 的 `dp[mask][j]` 求最优。迷宫是无向的，机关到石堆与石堆到机关的距离相同，所以只需从 `S`、`T` 和每个机关各做一次 BFS（至多 `18` 次）。

```python
from collections import deque
from math import inf


def minimal_steps(maze: list[str]) -> int:
    rows, cols = len(maze), len(maze[0])
    cells: dict[str, list[tuple[int, int]]] = {ch: [] for ch in "SMOT"}
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            if ch in cells:
                cells[ch].append((r, c))
    start, target = cells["S"][0], cells["T"][0]
    mech, stones = cells["M"], cells["O"]
    k = len(mech)

    def bfs(src: tuple[int, int]) -> list[list[float]]:    # 单源最短路，墙不可走；不可达为 inf
        dist = [[inf] * cols for _ in range(rows)]
        dist[src[0]][src[1]] = 0
        queue = deque([src])
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#" and dist[nr][nc] == inf:
                    dist[nr][nc] = dist[r][c] + 1
                    queue.append((nr, nc))
        return dist

    from_start = bfs(start)
    if k == 0:                              # 没有机关：直接走到宝藏
        d = from_start[target[0]][target[1]]
        return -1 if d == inf else int(d)
    from_target = bfs(target)
    # 迷宫是无向的：机关 -> 石堆 与 石堆 -> 机关 的距离相同，所以只需从每个机关 BFS 一次
    to_stone = [[d[r][c] for r, c in stones] for d in map(bfs, mech)]   # to_stone[i][s]：机关 i 到第 s 个石堆
    start_stone = [from_start[r][c] for r, c in stones]
    first = [min(a + b for a, b in zip(start_stone, to_stone[j])) for j in range(k)]   # S -> 石堆 -> 机关 j
    hop = [[min(a + b for a, b in zip(to_stone[i], to_stone[j])) for j in range(k)]    # 机关 i -> 石堆 -> 机关 j
           for i in range(k)]
    end = [from_target[r][c] for r, c in mech]                                          # 机关 i -> 宝藏
    # dp[mask][j]：已触发的机关集合是 mask，人刚好站在机关 j 上的最少步数
    full = 1 << k
    dp = [[inf] * k for _ in range(full)]
    for j in range(k):
        dp[1 << j][j] = first[j]
    for mask in range(1, full):
        for j in range(k):
            prev = mask ^ (1 << j)
            if mask >> j & 1 and prev:
                dp[mask][j] = min(dp[prev][i] + hop[i][j] for i in range(k) if prev >> i & 1)
    ans = min(dp[full - 1][j] + end[j] for j in range(k))
    return -1 if ans == inf else int(ans)
```

运行：`["S#O","M..","M.T"]` → `16`，`["S#O","M.#","M.T"]` → `-1`，`["S#O","M.T","M.."]` → `17`，`["ST"]` → `1`，`["S#T"]` → `-1`；`100 × 100`、`16` 个机关、`40` 个石堆的随机迷宫用时不到 `1` 秒。

**复杂度。** 时间：BFS 至多 `k + 2` 次，每次 `O(行 · 列)`；预计算 `hop` 是 `O(k^2 · |O|)`；DP 是 `O(2^k · k^2)`，约 `2^16 * 16 * 16 / 4 ≈ 4 * 10^6` 次转移。空间 `O(2^k · k)`。

**易错点。**
- 把机关间距离当成直接步行距离、忘了每次都要去石堆取石头：示例 1 会得到 `4`（`S→M→M→T`），正确是 `16`。
- 贪心「每次去最近的下一个机关」：`["TSO","MOM"]` 得到 `7`，正确是 `5`（先去远离宝藏的那个机关，最后一个机关紧挨 `T`）。
- 不可达要用 `inf` 参与 `min` 和加法，不要用 `-1`；`S` 到石堆不通、或机关被墙围住时答案是 `-1`。
- `M` 为 `0` 时没有 DP，直接 `BFS(S → T)`；漏掉这个分支会对空的 `mask` 取 `min` 报错。

**追问。**
- 要输出具体路线：`dp` 同时记录前驱 `(prev_mask, i)`，回溯得到机关触发顺序，再用各段 BFS 的前驱还原路径。
- 机关到 `20` 个以上：`2^20 * 20` 约两千万个状态，纯 Python 吃力，需要用位运算或 NumPy 向量化，或者换近似算法。
- 石堆很多（如上万个）：BFS 次数取 `min(机关数, 石堆数) + 2`，`hop` 的预计算 `O(k^2 · |O|)` 仍然很小。

**同模式。** LC 847 访问所有节点的最短路径、LC 943 最短超级串、LC 1125 最小的必要团队、LC 1994 好子集的数目、LC 526 优美的排列。
