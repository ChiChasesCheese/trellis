---
id: tlc-xun-bao-2-code
node: p5.xun-bao
type: qa
step: 2
---
## Q
**LCP 13 寻宝**｜写出 Python 实现

迷宫 `maze: list[str]`（最大 `100 × 100`）含 `S`（入口）、`T`（宝藏）、`M`（机关，至多 `16` 个，全部触发才能拿宝藏）、`O`（石堆，至多 `40` 个，石头无限、一次搬一块）、`#`（墙）、`.`（空地）。触发机关需要把石头放在它上面；搬起 / 放下不算步数，每步移动一格。返回最少步数，无法拿到宝藏返回 `-1`。

## A
**思路。** 用 BFS 得到 `S`、`T` 和每个机关到全图的距离。预计算 `first[j]`（`S → 石堆 → 机关 j`）、`hop[i][j]`（`机关 i → 石堆 → 机关 j`）和 `end[i]`（`机关 i → T`）。再对机关集合做状态压缩 DP，最后取 `dp[全集][j] + end[j]` 的最小值。

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

运行：`["S#O","M..","M.T"]` → `16`，`["S#O","M.#","M.T"]` → `-1`，`["S#O","M.T","M.."]` → `17`，`["ST"]` → `1`，`["S#T"]` → `-1`。

**复杂度。** 时间：至多 `k + 2` 次 BFS，各 `O(行 · 列)`；`hop` 预计算 `O(k^2 · |O|)`；DP 约 `O(2^k · k^2)`（实际转移数 `k(k-1)2^(k-2)`，`k = 16` 时约 `4 * 10^6`）。空间 `O(2^k · k + 行 · 列)`。

**写法要点。** 位运算表示集合：`1 << j` 是单元素集合，`mask >> j & 1` 判断含不含，`mask ^ (1 << j)` 去掉元素；`map(bfs, mech)` 对每个机关各跑一次 BFS；`zip` 加生成器 `min(a + b for a, b in zip(...))` 一行求出对所有石堆取最小；`inf` 参与加法和 `min` 自然传播「不可达」，最后统一转成 `-1`。
