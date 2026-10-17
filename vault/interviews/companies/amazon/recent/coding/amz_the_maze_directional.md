# 迷宫（The Maze）与方向约束 BFS（Directional-constraint BFS）

> 来源：1p3a 1190455（SDE II 店面，2026-09-16；帖子 2026-09-22）https://www.1point3acres.com/bbs/thread-1190455-1-1.html ；LC 490 题面镜像 https://leetcode.ca/all/490.html （官方页为付费题）。已有 Anki 卡 `forbidden-turn-grid`。
> 代码：`../../coding/solutions/490_the_maze.py`、`code/amz_directional_grid.py`。

## 面经原话
- 帖子摘要：40 分钟 BFS 带移动约束；「基本上每写几段，面试官就要问为什么这么写并且问你这么写对不对，最后压轴码完没有留时间走代码，结束复盘的时候发现三维向量存储写错了。」
- 回帖：「你这题写的。。不能回头不能左不能右转。。那还做啥。。。」；另一条回复认为接近 490 但带方向。**(reconstructed)** 原题的精确规则帖子没有写全；下文的变体是按这些碎片重建的，不是原文。

## 开场先问的澄清问题
1. 「方向约束」具体是哪几种：不能掉头？不能右转？转弯次数有上限？
2. 求的是「最短步数」还是「能不能到」？
3. 起点的初始朝向是给定的还是任选？
4. 一步是走一格，还是像 490 那样滚到撞墙才停？

## 先补一点基础：BFS 与「状态」
- BFS（广度优先搜索）按「距离」一层一层扩展，第一次到达某状态时的步数就是最短步数——前提是每条边代价相同。
- **状态（state）** 是「决定未来能怎么走的全部信息」。普通网格里状态是 (r, c)；一旦规则和「上一步朝向」有关，朝向必须进状态：(r, c, dir)。这就是帖子里说的「三维向量」。写错的常见点：visited 只存 (r, c)，会把「以不同朝向到达同一格」误判成已访问，从而漏掉合法路径。

## LC 490：球滚到撞墙才停
规则（来自镜像题面）：球向上/下/左/右滚，不撞墙不停；停下后才能换方向；问球能否**停**在终点。网格边长不超过 100，外圈视为墙。
- 最笨解：每个格子每个方向一步步走，状态 (r, c, dir) 的 DFS（见代码里的 `_brute`）。
- 改进：球「停下」的位置才是有意义的节点。每次从一个停点出发，往 4 个方向各滚到底，得到最多 4 条边。节点数 ≤ mn，每条边滚动 O(max(m,n))，总 O(mn·(m+n))。
- 注意：经过终点但没停下不算；所以判断终点要在**出队时**对停点判断，而不是在滚动路上。

```python
def has_path(maze, start, destination):
    m, n = len(maze), len(maze[0])
    seen = {tuple(start)}
    queue = deque([tuple(start)])
    while queue:
        r, c = queue.popleft()
        if [r, c] == list(destination):                  # must STOP here, not just pass through
            return True
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r, c
            while 0 <= nr + dr < m and 0 <= nc + dc < n and maze[nr + dr][nc + dc] == 0:
                nr, nc = nr + dr, nc + dc                # keep rolling until the next cell is wall / border
            if (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append((nr, nc))
    return False
```

## 重建的方向约束变体（reconstructed）
规则：每步走一格；新朝向只能是「保持不变」或「左转」，不能右转、不能掉头；起始朝向任选；求最少步数。
- 为什么 visited 要带朝向：同一格以「朝北」和「朝东」到达，接下来能走的方向集合不同。
- 状态数 4mn，每个状态最多 2 条出边，BFS O(mn)。
- 示例：3×3，中间是墙，从 (2,0) 到 (2,2) 是 2 步（一路向东）；在无墙的 2×2 网格里从 (0,1) 走到正下方 (1,1) 只要 1 步（朝南）。
- 若加「最多转 K 次」，状态变成 (r, c, dir, turns)，状态数乘以 K+1。

```python
HEADINGS = ((-1, 0), (0, 1), (1, 0), (0, -1))             # N E S W, so (h + 1) % 4 is a right turn and (h - 1) % 4 a left turn

def min_steps(grid, start, target):
    m, n = len(grid), len(grid[0])
    queue = deque((start[0], start[1], h, 0) for h in range(4))   # the first step may head anywhere
    seen = {(start[0], start[1], h) for h in range(4)}
    while queue:
        r, c, h, d = queue.popleft()
        if (r, c) == tuple(target):
            return d
        for nh in (h, (h - 1) % 4):                       # straight or left; right and reverse are simply not listed
            nr, nc = r + HEADINGS[nh][0], c + HEADINGS[nh][1]
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc, nh) not in seen:
                seen.add((nr, nc, nh))
                queue.append((nr, nc, nh, d + 1))
    return -1
```

## senior 追问
1. **转弯有代价（比如转一次 +5）**：边权不再相等，BFS 改 Dijkstra；状态不变。
2. **直行代价 0、转弯代价 1**：0-1 BFS（双端队列）即可，见 3286 的讲义。
3. **网格很大（1e4×1e4）**：状态数 4×1e8 放不下。可以按「直线段」建图：只在转弯点和终点建节点；或双向 BFS。
4. **多个终点/多个起点**：多源 BFS，把所有起点同时入队。
5. **输出路径**：状态里存前驱（parent）指针，到达终点后回溯。
6. **面试现场的做法**：先口述状态定义和转移（朝向进状态、转移表），再写代码；留 5 分钟用一个小例子手跑——帖子里的失误正是没有留走查时间。

## 自测题
1. 490 里为什么起点本身要先入队、终点要在出队时判断？
<details><summary>答案</summary>起点就是第一个「停点」；终点必须是停点，滚动途中经过终点不算到达。</details>
2. 变体里如果 visited 只存 (r, c) 会错在哪？
<details><summary>答案</summary>先到的路径可能朝向不利（比如只能再向左转），后到的路径朝向有利却被丢弃，最短路可能被剪掉。</details>
3. 变体中「右转和掉头不允许」，代码里为什么不用写 if 判断，只列 `(h, (h - 1) % 4)`？
<details><summary>答案</summary>候选朝向本身就只有直行和左转两种，不允许的转移根本没有生成。</details>
