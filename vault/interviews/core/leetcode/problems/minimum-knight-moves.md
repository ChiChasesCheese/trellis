---
slug: minimum-knight-moves
---
## Q
**LC 1197 进击的骑士**｜Medium

无限棋盘上骑士从 `(0, 0)` 走「日」字，求到 `(x, y)` 的最少步数。`|x| + |y| ≤ 300`。

## A
**一句话。** 每步代价相同，BFS 第一次到达即最短；棋盘对称，把目标折到第一象限，搜索框限制在 `[-2, x+2] × [-2, y+2]`。

```python
def min_knight_moves(x, y):
    x, y = abs(x), abs(y)          # 对称，折到第一象限
    moves = ((1, 2), (2, 1), (-1, 2), (-2, 1),
             (1, -2), (2, -1), (-1, -2), (-2, -1))
    q = deque([(0, 0)])
    seen = {(0, 0)}
    steps = 0
    while q:
        for _ in range(len(q)):    # 一层 = 一步
            r, c = q.popleft()
            if (r, c) == (x, y):
                return steps
            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if (-2 <= nr <= x + 2 and -2 <= nc <= y + 2
                        and (nr, nc) not in seen):
                    seen.add((nr, nc))
                    q.append((nr, nc))
        steps += 1
```

**复杂度。** 时间 `O(xy)`，空间 `O(xy)`。

**易错点。**
- 下界设成 `0`：`(1, 1)` 要绕到负坐标，答案是 `2`，限制在 `[0, …]` 会算错。
- 出队时才标记已访问：同一格重复入队，队列膨胀。

**追问。**
- 更快？：双向 BFS，或在大距离时先贪心逼近再 BFS 收尾。
- 有障碍物的有限棋盘？：同样 BFS，判断边界和障碍即可。

**同模式。** LC 127 单词接龙、LC 1091 二进制矩阵中的最短路径、LC 752 打开转盘锁
