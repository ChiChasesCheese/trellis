# 迷宫（The Maze）与方向约束 BFS（Directional-constraint BFS）

网格里有墙和空地，要从起点走到终点。经典的 LeetCode 490 里，球一旦朝某个方向滚动就不会自己停，要一直滚到撞墙才停，停下后才能换方向；问球能不能正好停在终点。另一类更常见的变形给移动加上方向限制，例如「不能掉头、不能右转」，问最少几步。这两类题的共同难点是：BFS 的「状态」不能只是坐标，要把决定下一步的全部信息放进去。

## 开场先问的澄清问题
1. 「方向约束」具体是哪几种：不能掉头？不能右转？转弯次数有上限？
2. 求的是「最短步数」还是「能不能到」？
3. 起点的初始朝向是给定的还是任选？
4. 一步是走一格，还是像 490 那样滚到撞墙才停？

## 先补一点基础：BFS 与「状态」
- BFS（广度优先搜索）按「距离」一层一层扩展，第一次到达某状态时的步数就是最短步数，前提是每条边代价相同。
- **状态（state）** 是「决定未来能怎么走的全部信息」。普通网格里状态是 (r, c)；一旦规则和「上一步朝向」有关，朝向必须进状态：(r, c, dir)，也就是三维的 visited。写错的常见点：visited 只存 (r, c)，会把「以不同朝向到达同一格」误判成已访问，从而漏掉合法路径。

## LC 490：球滚到撞墙才停
规则：球向上/下/左/右滚，不撞墙不停；停下后才能换方向；问球能否**停**在终点。网格边长不超过 100，外圈视为墙。
- 最笨解：每个格子每个方向一步步走，对状态 (r, c, dir) 做 DFS（见代码里的 `_brute`）。状态多、每步都要判断，慢。
- 改进：球「停下」的位置才是有意义的节点，滚动途中经过的格子没有选择可做。每次从一个停点出发，往 4 个方向各滚到底，得到最多 4 条边。节点数 ≤ mn，每条边滚动 O(max(m,n))，总 O(mn·(m+n))。
- 注意：经过终点但没停下不算到达；所以判断终点要在**出队时**对停点判断，而不是在滚动路上。

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

## 方向约束变体
规则：每步走一格；新朝向只能是「保持不变」或「左转」，不能右转、不能掉头；起始朝向任选；求最少步数。
- 为什么 visited 要带朝向：同一格以「朝北」和「朝东」到达，接下来能走的方向集合不同；先到的那条路若朝向不利，后到的朝向有利的路径不能被丢掉。
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
2. **直行代价 0、转弯代价 1**：0-1 BFS（双端队列）即可，参见安全路径一讲。
3. **网格很大（1e4×1e4）**：状态数 4×1e8 放不下。可以按「直线段」建图：只在转弯点和终点建节点；或双向 BFS。
4. **多个终点或多个起点**：多源 BFS，把所有起点同时入队。
5. **输出路径**：状态里存前驱（parent）指针，到达终点后回溯。
6. **现场的做法**：先口述状态定义和转移（朝向进状态、转移表），再写代码；留 5 分钟用一个小例子手跑。三维状态写错而没有留时间走查，是这类题最常见的失分点。

## 自测题
1. 490 里为什么起点本身要先入队、终点要在出队时判断？
<details><summary>答案</summary>起点就是第一个「停点」；终点必须是停点，滚动途中经过终点不算到达。</details>
2. 变体里如果 visited 只存 (r, c) 会错在哪？
<details><summary>答案</summary>先到的路径可能朝向不利（比如只能再向左转），后到的路径朝向有利却被丢弃，最短路可能被剪掉。</details>
3. 变体中「右转和掉头不允许」，代码里为什么不用写 if 判断，只列 `(h, (h - 1) % 4)`？
<details><summary>答案</summary>候选朝向本身就只有直行和左转两种，不允许的转移根本没有生成。</details>
