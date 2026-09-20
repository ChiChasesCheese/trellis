---
nodes: [problems.games.tic-tac-toe, method.modeling]
tags: [problem]
---
# Drill：井字棋（Tic-Tac-Toe）

最常见的热身题：两个人轮流在棋盘上落子，连成一条线就赢。真正被考的不是 3×3 那三行判断，
而是"写完之后还剩下什么"——棋盘变成 N×N、规则变成 K 子连珠、要能悔棋、一方换成电脑，
这四刀砍下来，你第 1 关写的类还站得住吗。按真实机考的节奏分关做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：3×3，两人轮流落子，三子连线获胜，满盘无线是和棋。棋局状态要显式
  （进行中／有人获胜／和棋），**和棋靠已落子数判定，不许扫盘**。四条非法路径——落在盘外、
  格子已被占、不是你的回合、棋局已结束——各抛一个有名字的异常，不准返回 `False`。
  写之前先回答：\"现在轮到谁\"是存一个字段，还是从走子历史算出来？把两个候选的代价都说出来。
- 第 2 关（约 15 分钟）：棋盘边长变成构造参数，胜负判定**每手不许扫全盘**。先做 K == N 的
  增量计数器版本（每行、每列、两条对角线各一个计数），再加上 K 子连珠（K < N）的泛化。
  做到这里你会撞上一堵墙：增量计数器在 K < N 时省不下任何东西。**想清楚为什么**，并决定
  这两种算法是共用一个接口，还是在棋盘里加一个 `if`。
- 第 3 关（约 15 分钟）：悔棋与重做，可以连悔任意多手。注意两件事：第 2 关引入的增量状态
  必须能**退回去**（并且计数降到 0 时把键删掉）；走出新的一手之后，重做栈必须清空，否则
  `redo()` 会接回一段从未发生的历史。暴露一个只读的深度属性，好让这两条能被断言。
- 第 4 关（选做，约 10 分钟）：接入电脑玩家——先随机，再做"能赢就赢、不能赢就堵、都不是
  就往中心靠"的一步启发式。验收标准很硬：**不许改动棋盘类和棋局类的任何一行**。
  随机数发生器必须是注入的，否则测试不可复现。

**怎么练**：把 `vault/domains/low-level-design/problems/tic-tac-toe/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/tic-tac-toe -q`。

**评分点**
- 说得出"每行每列加两条对角线的计数器是 O(1)"**只在 K == N 时成立**，K 子连珠没有等价的
  增量做法（[[problems-tic-tac-toe-o1-only-when-k-equals-n]]）。
- 把"刚才这一手赢了吗"和"我要是走这里会赢吗"分成两个问题：后者要一个不改状态的纯函数，
  起点格无条件算一子（[[problems-tic-tac-toe-two-win-questions]]）。
- 悔棋时增量计数能退回去，并且计数降到 0 时删键；用一个只读属性让"悔到空盘必须归零"可断言
  （[[problems-tic-tac-toe-counter-must-shrink]]、[[oop-getter-collection-leak]]）。
- 只有一种操作时拒绝命令模式，改用一条纯数据的走子记录，并说得出什么时候这个答案会翻转
  （[[problems-tic-tac-toe-undo-no-command]]、[[patterns-command-when]]）。
- "轮到谁"是走子历史的派生量而不是一个字段，因此悔棋、三人局都白送
  （[[problems-tic-tac-toe-turn-is-derived]]、[[method-invariant-ownership]]）。
- 非法着法不消耗回合，四种失败各有异常类型，调用方能分别处理也能一把兜住
  （[[problems-tic-tac-toe-illegal-move-order]]）。
- `Player` 只是不可变的身份加一个**可选的决策函数**，人类的那一格是 `None`；库代码里不出现
  `input()`（[[problems-tic-tac-toe-player-thin-strategy]]、[[oop-polymorphism-vs-switch]]）。
- 给机器人的是一个 `Protocol` 写成的只读契约加元组快照，而不是一个只会转发的只读包装类
  （[[problems-tic-tac-toe-readonly-view-protocol]]）。

**题解**：[[solution-tic-tac-toe]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
