# 安全路径（Find a Safe Walk Through a Grid, LC 3286）

一张 m×n 的网格，值为 1 的格子不安全，踩上去生命值减 1，值为 0 的格子安全。你从左上角出发，每次走上下左右一格，要走到右下角，并且到达时生命值至少还剩 1。问有没有这样的走法。难点是看穿它的本质：这是一道边权只有 0 和 1 的最短路，所以不需要把血量放进状态，也不需要完整的 Dijkstra，一个双端队列的 0-1 BFS 就够了。

## 题面与约束
`grid[i][j]` 为 1 的格子是不安全的，踩上去生命值 −1；从左上角走到右下角（四方向），到终点时生命值必须 ≥ 1，问是否可能。
约束：`m == grid.length`，`n == grid[i].length`，`1 <= m, n <= 50`，`2 <= m * n`，`1 <= health <= m + n`，`grid[i][j]` 为 0 或 1。

## 开场先问的澄清问题
1. 起点是不安全格子时，起点也扣血吗？（题面：是。）
2. 允许走回头路吗？（允许，但绝不会有帮助。）
3. 到终点时生命值正好为 1 算可以吗？（算，要求「大于 0」。）

## 先补一点基础：把问题改写成最短路
「到终点时血量 ≥ 1」等价于「路径上不安全格子总数 ≤ health − 1」。所以只要求出起点到终点**经过的不安全格子数的最小值** c，判断 `c < health`。每个格子的「进入代价」是 0 或 1，这就是边权只有 0 和 1 的最短路。

## 最笨解
DFS 枚举所有路径、记录血量。路径数指数级，50×50 完全不可行。

## 逐步改进
1. **BFS 状态加血量** (r, c, hp)：状态数 mn·health ≤ 2500·100，可行但笨重，且血量其实是多余的维度：只要最小代价已知，就能直接回答。
2. **Dijkstra**：把问题当边权 0/1 的最短路，O(mn log mn)。能做，但堆的 log 因子对只有两种边权来说是浪费。
3. **0-1 BFS**：普通 BFS 的队列按距离单调。边权 0 时把节点放**队首**，边权 1 时放**队尾**，队列里的距离依然保持单调（最多两种相邻取值），于是每个节点只需处理常数次，O(mn)。
4. 实现要点：`cost[nr][nc]` 初始 ∞；松弛成功才入队；起点的 cost 取 `grid[0][0]`。

```python
def find_safe_walk(grid, health):
    m, n = len(grid), len(grid[0])
    INF = float("inf")
    cost = [[INF] * n for _ in range(m)]
    cost[0][0] = grid[0][0]                               # the start cell also costs health if unsafe
    dq = deque([(0, 0)])
    while dq:
        r, c = dq.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                w = grid[nr][nc]
                if cost[r][c] + w < cost[nr][nc]:
                    cost[nr][nc] = cost[r][c] + w
                    if w == 0:
                        dq.appendleft((nr, nc))           # free edge: front of the deque keeps costs sorted
                    else:
                        dq.append((nr, nc))
    return cost[m - 1][n - 1] < health                    # health must stay >= 1 on arrival
```

示例：`[[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]]`，health = 1，沿下边绕过所有 1，最小代价 0 < 1，返回 True；`[[1,1,1],[1,0,1],[1,1,1]]`，health = 5：从角上进入需要踩 1，终点也是 1，最小代价 4 < 5，返回 True。

## 复杂度
m·n 个格子，每个最多入队 O(1) 次（常数 = 松弛成功次数，最多 2 次）：时间 O(mn)，空间 O(mn)。

## senior 追问
1. **为什么 0-1 BFS 队列仍有序**：队首元素距离为 d，队列中只有 d 与 d+1 两种值；0 边放前保持 d，1 边放后得到 d+1。
2. **格子上的伤害不止 1（权值 0..k）**：回到 Dijkstra，或桶式 BFS（k 小时用 k+1 个桶）。
3. **要输出一条最安全路径**：松弛时记录前驱，回溯。
4. **有回血格子（权值 −1）**：负权，Dijkstra 失效；改 Bellman-Ford / SPFA，并要判负环。
5. **网格 1e4×1e4**：O(mn) 的内存放不下，改成按行滚动或 A*（以曼哈顿距离为启发式，保持可采纳）。
6. **多次修改格子再查询**：动态最短路很难，先问清查询与修改比例，必要时离线批处理。

## 自测题
1. 为什么权值 0 的邻居要 `appendleft`？
<details><summary>答案</summary>它和当前节点距离相同，应当和当前节点一起尽早处理；放前面让队列保持距离非递减。</details>
2. 为什么最终比较是 `cost < health` 而不是 `<=`？
<details><summary>答案</summary>每个不安全格扣 1 点，到终点时剩余血量为 health − cost，需要 ≥ 1，即 cost ≤ health − 1。</details>
3. 起点是 1 时 `cost[0][0]` 该是多少？
<details><summary>答案</summary>1，起点也扣血。</details>

## 来源
- Hello Interview 社区题目 `safe-walk-grid`，约 2026-10-01，中级 APAC：https://www.hellointerview.com/community/questions/safe-walk-grid ；公司页 https://www.hellointerview.com/community/questions?company=Amazon 。
- 摘要：「Determine whether there's a 4-directional path from the top-left to bottom-right of an m×n binary grid ... so your health stays positive」。报告只有题目名，没有面试官的追问。
- LC 官方 https://leetcode.com/problems/find-a-safe-walk-through-a-grid/ （约束取自该页）。官方样例 1 和样例 2 即上文两个示例。
- 代码：`../../coding/solutions/3286_find_a_safe_walk_through_a_grid.py`。
