---
slug: snakes-and-ladders
---
## Q
**LC 909 蛇梯棋**｜Medium

`n x n` 棋盘按转行交替方式从左下角编号 `1..n^2`，每回合掷 6 面骰前进；格子值不为 `-1` 时传送到该编号（一回合只传送一次）。求从 `1` 到 `n^2` 的最少回合数，不可能返回 `-1`。

## A
**一句话。** 把方格当节点，每格向后 6 格连边（遇蛇梯改终点），在无权图上 BFS 求最短路。

```python
def snakes_and_ladders(board):
    n = len(board)
    end = n * n

    def cell(k):              # 编号 -> board 上的值
        r, c = divmod(k - 1, n)
        if r % 2:             # 从底往上数，奇数行反向
            c = n - 1 - c
        return board[n - 1 - r][c]

    dist = {1: 0}
    q = deque([1])
    while q:
        cur = q.popleft()
        for nxt in range(cur + 1, min(cur + 6, end) + 1):
            if cell(nxt) != -1:
                nxt = cell(nxt)   # 只传送一次
            if nxt == end:
                return dist[cur] + 1
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                q.append(nxt)
    return -1
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n^2)`。

**易错点。**
- 传送后继续传送：目的地又是蛇梯起点时规则不允许再传。
- 判断终点放在传送之前：梯子可能直接把你送到终点，要用传送后的 `nxt` 判断。
- 忘了奇数行反向，或用矩阵行号而不是「从底往上数」的行号判奇偶。

**追问。**
- 骰子面数变成 `k`？：把 `6` 换成 `k`。
- 可以选择是否传送？：每格有两个后继，同样 BFS。

**同模式。** LC 127 单词接龙、LC 752 打开转盘锁、LC 1091 二进制矩阵中的最短路径、LC 773 滑动谜题
