# 棋子最少步数吃掉国王（Chess piece to king, min moves）

棋盘上有一枚己方棋子和对方的国王（king）。棋子每回合按自己的走法走一步，落在国王所在的格子就是吃掉国王。问最少几步能吃到。这是一道最短路题：每一步代价相同，所以用 BFS。难点不在 BFS 本身，而在走法的生成（跳着走还是滑着走、会不会被挡住），以及棋子变多时「状态」怎样表示。

棋盘大小、走法、障碍这些设定题面不会全给，要逐项向面试官确认。下面的解法按单个棋子、多个棋子两种情况都写出来。

## 开场先问的澄清问题
1. 棋盘多大？是否有障碍或己方其他棋子挡路？
2. 棋子是哪一种？走法是固定偏移（马、国王），还是滑动（车、象，会被挡住）？
3. 吃掉 king 是「走到 king 所在的格子」吗？king 会动吗？
4. 只有一枚棋子在动，还是每回合可以选己方任意一枚？
5. 不可达时返回 -1？

## 先补一点基础：BFS 与「状态压缩」
- **BFS**：每步代价相同的最短路，按层扩展，第一次到达就是最短。
- **状态（state）**：「当前局面里决定后续的所有信息」。单个棋子、king 不动：状态就是棋子的位置 (r, c)，n×n 个。
- **状态压缩**：多个棋子时，状态 = 所有己方棋子位置的元组；每个位置编码成 `r*n+c`，一个棋盘位可以放进整数或位集合里。k 个棋子最多 (n²)^k 个状态，所以 k 很小才可行（8×8 的两个棋子约 4096 个状态，三个约 26 万）。

## 最笨解
递归枚举所有走法序列，深度从 1 开始逐步加深（迭代加深 DFS），指数级；仅在小棋盘上用于核对结果（`_brute`）。

## 逐步改进
1. **问题**：同一个位置会被重复访问，枚举走法序列的数量随步数指数增长。
2. **想法**：BFS，`seen` 记录已到达的位置；第一次走到 king 的格子即返回步数。每个位置只展开一次，状态数 n² 就是上界。
3. **走法生成**：马、国王是固定偏移，只需检查是否越界、是否落在己方棋子上；车是滑动的：沿一个方向一格一格走，遇到己方棋子停下，**停下之前经过的每个格子都是合法落点**。
4. **king 不是障碍**：落在 king 上就是吃掉，立即返回 `d + 1`；如果把 king 当障碍，就永远吃不到。
5. **多个己方棋子的扩展**：每回合只能动一枚，其他棋子成为它的障碍，所以状态必须变成所有位置的元组，BFS 的结构不变。

```python
KNIGHT = ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1))
KING = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
ROOK_DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def moves(kind, pos, n, blocked):
    r, c = pos
    if kind in ("knight", "king"):                        # jumpers: one fixed offset, land on any non-blocked square
        for dr, dc in (KNIGHT if kind == "knight" else KING):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in blocked:
                yield nr, nc
    else:                                                 # rook: slide until the board edge or a blocker
        for dr, dc in ROOK_DIRS:
            nr, nc = r + dr, c + dc
            while 0 <= nr < n and 0 <= nc < n and (nr, nc) not in blocked:
                yield nr, nc
                nr, nc = nr + dr, nc + dc

def min_moves_to_capture(n, kind, start, king, blocked=frozenset()):
    """blocked = squares of own pieces. The king square is NOT blocked: landing on it is the capture."""
    blocked = set(blocked)
    seen, queue = {start}, deque([(start, 0)])
    while queue:
        pos, d = queue.popleft()
        for nxt in moves(kind, pos, n, blocked):
            if nxt == king:
                return d + 1
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, d + 1))
    return -1

def min_moves_team(n, pieces, king):
    """pieces = [(kind, pos), ...]; one piece moves per turn, the others block. State = tuple of all positions."""
    start = tuple(p for _, p in pieces)
    kinds = [k for k, _ in pieces]
    seen, queue = {start}, deque([(start, 0)])
    while queue:
        state, d = queue.popleft()
        for i, kind in enumerate(kinds):
            others = set(state[:i] + state[i + 1:])
            for nxt in moves(kind, state[i], n, others):
                if nxt == king:
                    return d + 1
                new = state[:i] + (nxt,) + state[i + 1:]
                if new not in seen:
                    seen.add(new)
                    queue.append((new, d + 1))
    return -1
```

示例：8×8 空棋盘，从 (0,0) 到 (7,7)：马 6 步，国王 7 步，车 2 步（先横后竖）。3×3 里车在 (0,0)，king 在 (0,2)，(0,1)(1,0)(1,1) 被己方棋子占满，答案 -1。4×4 里车 (0,0)、马 (0,1)、king (0,3)：马先让开、车再滑过去，答案 2。

## 复杂度
单个棋子：状态 n²，每个状态的走法数 w（马/国王 8，车最多 4(n−1)），时间 O(n²·w)。k 个棋子：状态 (n²)^k，时间 O(k·w·(n²)^k)。

## senior 追问
1. **对方 king 会走**：变成双人博弈，状态加上 king 的位置和轮到谁；求「最少几步保证吃到」要用极小极大（minimax）或反向归纳（retrograde analysis）。
2. **吃子之外还有「被将军」约束**：走法生成之后过滤「走完后己方 king 被攻击」的走法。
3. **棋盘很大**：双向 BFS（从 king 反向走）或 A*（启发函数用切比雪夫距离或马步下界）。
4. **多个终点（多个敌 king）或多个起点**：多源 BFS。
5. **状态压缩的实现**：位置编码成整数，`frozenset` 或排序后的元组去重（棋子同类时顺序无关）。
6. **输出具体走法**：BFS 存前驱，回溯。

## 自测题
1. 车为什么不能「穿过」己方棋子？
<details><summary>答案</summary>滑动棋子沿一个方向走，遇到阻挡物就停；代码在遇到 `blocked` 时终止 while。</details>
2. 为什么 king 的格子不放进 `blocked`？
<details><summary>答案</summary>落到 king 上就是吃掉，需要被当作合法落点；若放进 blocked 就永远吃不到。</details>
3. 两枚己方棋子时，为什么不能把它们的最短步数简单相加？
<details><summary>答案</summary>每回合只能动一枚，且它们互相当障碍，状态必须一起记录。</details>
