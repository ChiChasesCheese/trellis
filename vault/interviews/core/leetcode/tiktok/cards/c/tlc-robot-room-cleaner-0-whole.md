---
id: tlc-robot-room-cleaner-0-whole
node: c.robot-room-cleaner
type: qa
---
## Q
**LC 489 扫地机器人**｜Hard · LC TikTok 全时段热度 41/100

房间是一个 `m x n` 的二进制网格（`0` 障碍物，`1` 空格子），机器人在未知的空格子里出发，初始朝向向上，四周被墙包围，所有空格子都能从起点走到。你拿不到网格，只能用 `Robot` 的四个 API：`move()`（前方是空格就前进并返回 `true`，是障碍就原地不动返回 `false`）、`turnLeft()`、`turnRight()`（各转 90 度）、`clean()`（清理当前格）。要求清理房间里每个空格子。`1 <= m <= 100`，`1 <= n <= 200`。例：`room = [[1]]` 起点 `(0, 0)` → 清理 1 个格子。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把起点当作相对坐标 `(0, 0)`，对四个方向做 DFS 回溯：能走且没去过就走过去递归，递归返回后物理退回来并恢复朝向。

**识别。** 「看不到地图，只能边走边探索，要求覆盖全部可达格子」：迷宫 DFS 加访问集合，坐标用相对起点的偏移。和普通网格 DFS 的差别是机器人有朝向、有物理状态，回溯时必须把位置和朝向都还原。

**推导。** 无法随机游走：不知道何时算清完。起点坐标未知但不影响，用 `(0, 0)` 记号即可，访问集合 `visited` 去重。每个格子按顺时针尝试四个方向，进入格子时朝向是 `d`，每试一个方向就 `turnRight()`，转满四次朝向回到 `d`。递归返回后机器人站在邻格、朝向仍是进入方向，掉头走回来再掉头，状态与递归前一致。

```python
def clean_room(robot: "Robot") -> None:
    DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))    # 上右下左：顺时针，和 turnRight 的转向一致
    visited: set[tuple[int, int]] = set()

    def go_back() -> None:
        robot.turnRight()                        # 掉头 -> 退一步 -> 掉头，位置回到来处且朝向不变
        robot.turnRight()
        robot.move()
        robot.turnRight()
        robot.turnRight()

    def dfs(x: int, y: int, d: int) -> None:     # 机器人站在 (x, y)，朝向 DIRS[d]
        visited.add((x, y))
        robot.clean()
        for k in range(4):
            nd = (d + k) % 4                     # 本轮面向的方向
            nx, ny = x + DIRS[nd][0], y + DIRS[nd][1]
            if (nx, ny) not in visited and robot.move():   # 先判访问再 move：去过的格子不浪费一步
                dfs(nx, ny, nd)
                go_back()
            robot.turnRight()                    # 无论走没走，都转到下一个方向

    dfs(0, 0, 0)
```

运行：`room = [[1]]` 清理 1 格；示例 1 的房间（`row = 1, col = 3`）清理其 `30` 个空格子，机器人回到起点且朝向向上；一条 `1 x 200` 的走廊（起点在中间）清理 200 格。

**复杂度。** 时间 `O(N)`（`N` 为空格子数，每格最多试 4 个方向，每次 `O(1)` 个 API 调用），空间 `O(N)`（`visited` 加递归栈）。

**拓展优化。**
- 递归深度可达 `N`（蛇形房间约 `m * n / 2` 格），默认递归上限会抛 `RecursionError`；显式栈版本见追问。
- 要求少转弯：能沿当前朝向继续走时先走，减少 `turnRight` 次数，复杂度不变。

**易错点。**
- 回溯时只退步不还原朝向：掉头的两次 `turnRight()` 要成对出现，否则外层循环的方向全乱，后面的格子会漏扫。
- 先 `move()` 再判断是否访问过：机器人已经走进去了，却没有 `dfs` 也没有退回来，位置丢失。
- 最坏深度：蛇形走廊里递归深度约 `10000`，CPython 默认上限约 1000，会抛 `RecursionError`，要 `sys.setrecursionlimit` 调高或改用显式栈。

**追问。**
- 递归深度超限：显式栈，每帧记录 `(x, y, d, 已试方向数 k)`。

```python
def clean_room_iter(robot: "Robot") -> None:
    DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))
    visited = {(0, 0)}
    robot.clean()
    stack: list[list[int]] = [[0, 0, 0, 0]]      # 每帧 [x, y, d, k]：k 是已经尝试过的方向数
    while stack:
        frame = stack[-1]
        x, y, d, k = frame
        if k == 4:                               # 四个方向都试完：弹出，物理退回父格
            stack.pop()
            if stack:
                robot.turnRight(); robot.turnRight()
                robot.move()
                robot.turnRight(); robot.turnRight()
                robot.turnRight()                # 对应父帧循环末尾的 turnRight
                stack[-1][3] += 1
            continue
        nd = (d + k) % 4
        nx, ny = x + DIRS[nd][0], y + DIRS[nd][1]
        if (nx, ny) not in visited and robot.move():
            visited.add((nx, ny))
            robot.clean()
            stack.append([nx, ny, nd, 0])        # 新帧的朝向正是 nd
        else:
            robot.turnRight()
            frame[3] += 1
```

**同模式。** LC 490 迷宫、LC 200 岛屿数量、LC 79 单词搜索、LC 733 图像渲染、LC 1197 骑士的最小步数。
