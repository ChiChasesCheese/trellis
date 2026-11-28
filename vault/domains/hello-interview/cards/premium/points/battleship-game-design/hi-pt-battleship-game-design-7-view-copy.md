---
id: hi-pt-battleship-game-design-7-view-copy
node: qb.lld.battleship-game-design.points
type: qa
step: 7
---
## Q
**海战棋 · 视图不泄露**｜追问 · 出自：海战棋 › 逐步扩展 1

`board_view(viewer, owner)` 要返回什么？怎么保证不泄露对手的船位，又不会被调用方改坏游戏？

## A
**显示规则。** `.` 未知，`o` 落空，`X` 命中；只有 `viewer == owner` 时，没被打到的船格才显示 `#`。对手的船位只通过已被打过的格子泄露。

**副本。** 每次现拼一个新的字符串列表返回，调用方改它不影响游戏。

**易错。** 直接把内部字典或列表返回给调用方。
