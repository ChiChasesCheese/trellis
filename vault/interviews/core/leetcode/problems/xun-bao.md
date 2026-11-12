---
slug: xun-bao
---
## Q
**LCP 13 寻宝**｜Hard

迷宫中 `S` 是入口，`T` 是宝藏，`#` 是墙。必须触发所有机关 `M` 才能拿宝藏：触发机关要把一块重石放上去，重石来自石堆 `O`（无限，但每次只能搬一块）。求最少步数，无法拿到返回 `-1`。机关至多 16 个。例：`["S#O","M..","M.T"]` → `16`。

## A
**一句话。** BFS 把「机关 `i` 去石堆取石再放到机关 `j`」压成边权 `hop[i][j]`，再对机关做状态压缩 DP（旅行商 TSP），最后加上到宝藏的距离。

```python
def minimal_steps(maze):
    R, C = len(maze), len(maze[0])
    cells = {ch: [] for ch in "SMOT"}
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            if ch in cells:
                cells[ch].append((r, c))
    start, target = cells["S"][0], cells["T"][0]
    mech, stones = cells["M"], cells["O"]
    k = len(mech)

    def bfs(src):       # 单源最短路，不可达为 inf
        dist = [[inf] * C for _ in range(R)]
        dist[src[0]][src[1]] = 0
        q = deque([src])
        while q:
            r, c = q.popleft()
            for a, b in (r+1,c), (r-1,c), (r,c+1), (r,c-1):
                if (0 <= a < R and 0 <= b < C
                        and maze[a][b] != "#"
                        and dist[a][b] == inf):
                    dist[a][b] = dist[r][c] + 1
                    q.append((a, b))
        return dist

    fs = bfs(start)
    if k == 0:          # 没有机关：直接走到宝藏
        d = fs[target[0]][target[1]]
        return -1 if d == inf else int(d)
    ft = bfs(target)
    # 迷宫无向：机关到石堆与石堆到机关距离相同
    ts = [[d[r][c] for r, c in stones]
          for d in map(bfs, mech)]
    ss = [fs[r][c] for r, c in stones]
    first = [min(a + b for a, b in zip(ss, ts[j]))
             for j in range(k)]         # S -> 石堆 -> 机关 j
    hop = [[min(a + b for a, b in zip(ts[i], ts[j]))
            for j in range(k)] for i in range(k)]
    end = [ft[r][c] for r, c in mech]   # 机关 -> 宝藏
    # dp[mask][j]：已触发集合 mask，站在机关 j 的最少步数
    full = 1 << k
    dp = [[inf] * k for _ in range(full)]
    for j in range(k):
        dp[1 << j][j] = first[j]
    for mask in range(1, full):
        for j in range(k):
            prev = mask ^ (1 << j)
            if mask >> j & 1 and prev:
                dp[mask][j] = min(dp[prev][i] + hop[i][j]
                                  for i in range(k)
                                  if prev >> i & 1)
    ans = min(dp[full - 1][j] + end[j] for j in range(k))
    return -1 if ans == inf else int(ans)
```

**复杂度。** 时间 `O(k·RC + k²|O| + 2^k·k²)`，空间 `O(2^k·k)`。

**易错点。**
- 机关间距离当成直接步行距离：忘了每次都要去石堆取石，示例得 `4`，应为 `16`。
- 贪心「每次去最近的机关」：`["TSO","MOM"]` 得 `7`，应为 `5`。
- 不可达用 `-1` 参与 `min`：要用 `inf`，不可达时最后才转成 `-1`。
- 没有机关时漏掉直接 BFS 的分支：对空 `mask` 取 `min` 会报错。

**追问。**
- 要输出具体路线？：`dp` 同时记前驱 `(prev_mask, i)`，回溯机关顺序，再还原各段 BFS 路径。
- 机关到 20 个以上？：约两千万个状态，纯 Python 吃力，需位运算向量化（NumPy）。

**同模式。** LC 847 访问所有节点的最短路径、LC 943 最短超级串、LC 1125 最小的必要团队、LC 526 优美的排列
