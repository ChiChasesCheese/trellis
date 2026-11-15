---
slug: find-winner-on-a-tic-tac-toe-game
---
## Q
**LC 1275 找出井字棋的获胜者**｜Easy

`3×3` 井字棋，`A` 先手（`X`），`B` 后手（`O`），`moves[i] = [行, 列]` 依次是落子位置，保证合法。返回 `"A"`、`"B"`，平局 `"Draw"`，没下完 `"Pending"`。

## A
**一句话。** 为 3 行、3 列、2 条对角线各设一个计数，`A` 落子加 1、`B` 落子减 1，谁的某个计数达到 `±3` 就赢。

```python
def tictactoe(moves):
    cnt = [0] * 8                  # 3 行 + 3 列 + 2 对角线
    for k, (r, c) in enumerate(moves):
        p = 1 if k % 2 == 0 else -1    # A 加 1，B 减 1
        cnt[r] += p
        cnt[3 + c] += p
        if r == c:
            cnt[6] += p            # 主对角线
        if r + c == 2:
            cnt[7] += p            # 副对角线
    for x in cnt:
        if x == 3:
            return 'A'
        if x == -3:
            return 'B'
    return 'Draw' if len(moves) == 9 else 'Pending'
```

**复杂度。** 时间 `O(moves)`，空间 `O(1)`。

**易错点。**
- 谁先落子：偶数步（从 0 起）是 `A`，奇数步是 `B`。
- 中心点只加一条对角线：`(1,1)` 同时在两条对角线上，两条都要加。
- 先判平局再判胜负：第 9 步也可能赢，要先看是否有人达到 `±3`。

**追问。**
- 在线判断每步后是否获胜？：落子后立刻检查该点所在的行、列、对角线的计数，`O(1)` 每步，就是 LC 348。
- 推广到 `n×n`？：计数数组长 `2n+2`，达到 `±n` 为胜。

**同模式。** LC 348 设计井字棋、LC 794 有效的井字游戏、LC 1958 检查操作是否合法、LC 36 有效的数独
