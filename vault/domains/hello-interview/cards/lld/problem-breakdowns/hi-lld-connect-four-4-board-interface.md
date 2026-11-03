---
id: hi-lld-connect-four-4-board-interface
node: lld.problem-breakdowns.connect-four.exam
type: qa
step: 4
---
## Q
**Board 的状态与接口**｜低层设计 · 题目拆解

Board 要保存什么、对外暴露哪些方法，才能让 Game 不碰网格细节？格子里存 Player 还是颜色？

## A
**要点。** 状态：行数 6、列数 7、`grid[rows][cols]`，空格为 null，否则是棋色。

方法：`canPlace(col)`、`placeDisc(col, color) -> row`（返回落点行，失败返回 -1）、`isFull()`、`checkWin(row, col, color)`、`getCell(row, col)`。

**为什么。** 格子里存 `DiscColor` 而不是 `Player`：类型更简单，测试 Board 时不用造 Player 对象。`placeDisc` 返回落点行，Game 不用重新扫描，就能把 `(row, col, color)` 交给 `checkWin`。

**取舍。** 所有边界与满列校验都放在 `placeDisc` 内，Game 只看返回值是不是 -1，而不是先调 `canPlace` 再落子，校验集中在一处。想优化可维护每列下一个空行的 `heights[cols]`，对 7x6 的盘面，简单循环就够了。
