---
id: hi-lld-connect-four-9-extensions
node: lld.problem-breakdowns.connect-four
type: qa
step: 9
---
## Q
**扩展追问：棋盘大小、悔棋、电脑对手**｜低层设计 · 题目拆解

面试官追问：支持不同棋盘大小、悔棋、加一个电脑对手，各自改动落在哪个类？

## A
**要点。**

- 棋盘大小：把 `rows`、`cols` 变成 `Board` 构造参数。放置与判胜逻辑本来就依赖这两个值和 `inBounds`，Game 只需决定造多大的盘。
- 悔棋：属于 Game，它掌管生命周期和回合。所有走棋都经过 `makeMove` 这个唯一入口，于是在那里记录一个 `Move(player, row, col)` 压栈；撤销时弹栈、让 Board 加一个 `clearCell` 清格、恢复当前玩家、状态重置为进行中、`winner` 置空。
- 电脑对手：规则不变。加一个 `BotEngine.chooseMove(game) -> col`，游戏循环里轮到机器人就调它，再走 `makeMove`。Board 与 Game 都不改。

**取舍。** 另一种做法是把 Player 做成接口，分 HumanPlayer 与 BotPlayer。更好的是保持 Player 纯数据，把「身份」和「决策」拆开，避免没有价值的抽象。
