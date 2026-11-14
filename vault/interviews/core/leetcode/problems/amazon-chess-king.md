---
slug: amazon-chess-king
---
## Q
**棋子吃掉国王的最少步数**｜Medium

`n × n` 棋盘上己方一枚棋子（马、王或车）在 `start`，对方国王在 `king` 不动；`blocked` 是己方其他棋子，不能落脚，车也不能穿过。求吃到国王的最少步数，不可达返回 `-1`。

## A
**一句话。** 棋子位置是 BFS 状态，走法生成器按棋子类型给落点（马和王走固定偏移，车沿方向滑到边或障碍前，途中每格都能停），第一次落到国王格就是答案。

```python
KNIGHT = ((1, 2), (2, 1), (-1, 2), (-2, 1),
          (1, -2), (2, -1), (-1, -2), (-2, -1))
KING = ((1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1))

def min_moves(n, kind, start, king, blocked):
    def free(x, y):
        return (0 <= x < n and 0 <= y < n
                and (x, y) not in blocked)

    def moves(r, c):
        if kind == "rook":    # 一路滑，途中每格都能停
            for dr, dc in KING[:4]:
                x, y = r + dr, c + dc
                while free(x, y):
                    yield x, y
                    x, y = x + dr, y + dc
        else:
            step = KNIGHT if kind == "knight" else KING
            for dr, dc in step:
                if free(r + dr, c + dc):
                    yield r + dr, c + dc

    start, king = tuple(start), tuple(king)
    seen, q = {start}, deque([(start, 0)])
    while q:
        (r, c), d = q.popleft()
        for p in moves(r, c):
            if p == king:     # 落到国王格就是吃掉
                return d + 1
            if p not in seen:
                seen.add(p)
                q.append((p, d + 1))
    return -1
```

**复杂度。** 时间 `O(n² · w)`，`w` 是单格走法数（车为 `O(n)`）；空间 `O(n²)`。

**易错点。**
- 把国王格也放进 `blocked`：永远落不上去，答案恒为 `-1`。
- 车滑动遇到障碍不停：会穿过己方棋子落到后面。

**追问。**
- 己方多枚棋子轮流走？：状态变成所有棋子位置的元组，状态数随棋子数指数增长，只适合很小的规模。
- 马在无限棋盘上（LC 1197）？：按对称折到第一象限并限制搜索框，或双向 BFS。

**同模式。** LC 994 腐烂的橘子、LC 1197 进击的骑士、LC 1091 二进制矩阵中的最短路径、LC 1222 可以攻击国王的皇后
