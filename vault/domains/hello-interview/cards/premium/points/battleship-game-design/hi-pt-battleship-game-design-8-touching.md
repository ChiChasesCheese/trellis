---
id: hi-pt-battleship-game-design-8-touching
node: qb.lld.battleship-game-design.points
type: qa
step: 8
---
## Q
**海战棋 · 相邻检查**｜追问 · 出自：海战棋 › 深入 6

`touching_allowed=False` 时怎么检查一艘船的每个格子是否与自己已有的船相邻？只查上下左右够吗？

## A
**不够。** 要含斜角：对每个格子查九宫格 `(dr, dc)`，`dr`、`dc` 各取 -1、0、1，里面有自己的船就拒绝。

```python
any((r + dr, c + dc) in side.at
    for dr in (-1, 0, 1) for dc in (-1, 0, 1))
```
**范围。** 只查自己的船，对手的船不算：两块棋盘是分开的。
