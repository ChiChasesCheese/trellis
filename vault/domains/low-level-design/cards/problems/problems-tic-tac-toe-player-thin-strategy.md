---
id: problems-tic-tac-toe-player-thin-strategy
node: problems.games.tic-tac-toe
type: qa
step: 7
tags: [grown]
---
## Q
井字棋的机考第 4 关会要求"把一方换成电脑玩家，而且不许改棋盘和棋局类"。如果 `Player` 被设计成抽象基类、`HumanPlayer.choose_move()` 里调 `input()` 读坐标，会有什么问题？更好的建模是什么？

## A
问题有两个。一是把 I/O 拖进了库代码：棋局一旦主动调 `choose_move`，它就只能在有 stdin 的地方被驱动，测试要么伪造标准输入、要么绕开棋局类。二是为"只差一个字段"的区别开了一棵继承树。

更好的建模：`Player` 是不可变的身份（名字、棋子符号）加一个**可选的决策函数** `strategy: Callable[[BoardView, str], Cell] | None`。人类的 `strategy` 是 `None`——他的决策本来就不在进程里，由外部调 `game.play(cell)` 给出；机器人只是把一个闭包塞进同一个字段。棋局提供两个入口：`play(cell)`（外部给出）和 `play_turn()`（问当前玩家要）。两个入口第 1 关就存在，所以加机器人时棋盘和棋局一行都不用动。
