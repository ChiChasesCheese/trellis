---
slug: robot-room-cleaner
---
## Q
**LC 489 扫地机器人**｜Hard

未知房间里，机器人只有 `move()`、`turnLeft()`、`turnRight()`、`clean()` 四个 API，要求清理所有可达的空格。

## A
**一句话。** 以起点为相对坐标 `(0,0)` 做 DFS 回溯：能走且没去过就走，返回后物理退回并恢复朝向。

```python
def clean_room(robot):
    DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))   # 上右下左，顺时针
    seen = set()

    def back():         # 掉头、退一步、掉头：位置回来，朝向不变
        robot.turnRight()
        robot.turnRight()
        robot.move()
        robot.turnRight()
        robot.turnRight()

    def dfs(x, y, d):
        seen.add((x, y))
        robot.clean()
        for k in range(4):
            nd = (d + k) % 4
            nx, ny = x + DIRS[nd][0], y + DIRS[nd][1]
            if (nx, ny) not in seen and robot.move():
                dfs(nx, ny, nd)
                back()
            robot.turnRight()   # 无论走没走都转向下一个方向

    dfs(0, 0, 0)
```

**复杂度。** 时间 `O(N)`，空间 `O(N)`（`N` 为空格数）。

**易错点。**
- 回溯只退步不还原朝向：掉头的两次 `turnRight` 要成对，否则后面方向全乱，漏扫。
- 先 `move()` 再判是否访问过：机器人已走进去却没有递归也没退回，位置丢失。
- 蛇形走廊递归深度约 `10^4`：超过 CPython 默认上限，抛 `RecursionError`。

**追问。**
- 为什么用相对坐标？：地图未知，只要起点算 `(0,0)`，`seen` 用相对坐标就够。
- 递归太深怎么办？：改显式栈，每帧记 `(x, y, d, 已试方向数)`。

**同模式。** LC 490 迷宫、LC 200 岛屿数量、LC 79 单词搜索、LC 733 图像渲染
