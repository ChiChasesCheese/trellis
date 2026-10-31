---
id: tlc-snakes-and-ladders-0-whole
node: c.snakes-and-ladders
type: qa
---
## Q
**LC 909 蛇梯棋**｜Medium · LC TikTok 全时段热度 38/100

`n x n` 的整数矩阵 `board`，方格按 `1..n^2` 编号，采用转行交替方式：从左下角 `board[n-1][0]` 开始编号，每一行方向反过来（第一行从左到右，第二行从右到左……）。你从方格 `1` 出发，每回合选一个目标方格 `next ∈ [curr + 1, min(curr + 6, n^2)]`（相当于掷 6 面骰子）。如果 `board[r][c] != -1`，那里有蛇或梯子，到达该格就被传送到 `board[r][c]`；一次掷骰中最多传送一次，就算目的地是另一条蛇或梯子的起点也不能继续。到达 `n^2` 游戏结束。返回到达 `n^2` 的最少掷骰次数，不可能则返回 `-1`。`2 <= n <= 20`，`board[i][j]` 为 `-1` 或在 `[1, n^2]` 内，方格 `1` 和 `n^2` 上没有蛇或梯子。例：`board = [[-1,-1],[-1,3]]` → `1`；题面的 `6 x 6` 示例 → `4`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把方格 `1..n^2` 当图的节点，每个方格向后 6 格连边（遇蛇梯改终点），在这张无权图上做 BFS 求最短路。

**识别。** 「每步代价相同、求最少步数」：BFS，状态就是当前方格编号。题目的难点是把编号换算成行列（转行交替）和蛇梯只传送一次。

**推导。** 暴力 DFS 枚举掷骰序列会指数爆炸，还要防环。每次掷骰花费 1，所以首次到达某个方格的步数就是最小步数，BFS 一层层扩展，`visited` 防止重复。编号 `label` 的行列：`r, c = divmod(label - 1, n)`，`r` 是从底向上数的行；奇数行反向，列 `c = n - 1 - c`；对应矩阵行 `n - 1 - r`。

```python
from collections import deque


def snakes_and_ladders(board: list[list[int]]) -> int:
    n = len(board)
    target = n * n

    def cell(label: int) -> int:                 # 方格编号 -> board 上的值
        r, c = divmod(label - 1, n)              # r：从底行向上数的行号
        if r % 2:                                # 奇数行方向反转
            c = n - 1 - c
        return board[n - 1 - r][c]

    dist = [-1] * (target + 1)                   # dist[label]：到达该格的最少掷骰数，-1 表示未到过
    dist[1] = 0
    queue = deque([1])
    while queue:
        cur = queue.popleft()
        for nxt in range(cur + 1, min(cur + 6, target) + 1):
            dest = cell(nxt)
            if dest != -1:                       # 有蛇或梯子：传送，且不再继续传送
                nxt = dest
            if nxt == target:
                return dist[cur] + 1
            if dist[nxt] == -1:
                dist[nxt] = dist[cur] + 1
                queue.append(nxt)
    return -1
```

运行：`[[-1,-1],[-1,3]]` → `1`，题面 `6 x 6` 示例 → `4`；`[[-1,-1],[-1,-1]]` → `1`（方格 1 掷 3 点直达 4）；全空的 `3 x 3` 棋盘 → `2`（`1 -> 7 -> 9`）。

**复杂度。** 时间 `O(n^2)`（每个方格出队一次，扩展 6 条边），空间 `O(n^2)`。

**拓展优化。**
- 要输出路径：用 `prev[nxt] = cur` 记录前驱，到达终点后回溯。
- 从两端同时 BFS（双向 BFS）能减少访问量，但图只有 `400` 个节点，一般不值得。

**易错点。**
- 传送后继续传送：目的地本身又是蛇梯起点时，规则明确不能再传，代码里只取一次 `cell(nxt)`。
- 到达终点的判断放在传送之前：`nxt == target` 要在替换为 `dest` 之后判断，因为梯子可能直接把你送到终点。
- 行列换算：忘了奇数行反向，或者对 `r` 的奇偶性判断用了矩阵行号而不是「从底往上数」的行号。

**追问。**
- 骰子面数变成 `k`：把 `6` 换成 `k`。
- 允许在梯子和蛇上选择是否传送：每个方格有两个后继，同样 BFS。

**同模式。** LC 127 单词接龙、LC 752 打开转盘锁、LC 1091 二进制矩阵中的最短路径、LC 773 滑动谜题、LC 365 水壶问题。
