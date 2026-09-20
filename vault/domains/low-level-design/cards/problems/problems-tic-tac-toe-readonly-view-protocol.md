---
id: problems-tic-tac-toe-readonly-view-protocol
node: problems.games.tic-tac-toe
type: qa
step: 8
tags: [grown]
---
## Q
井字棋的电脑玩家需要看盘面。把真正的棋盘对象传给它，它就能调 `place()` 改棋盘。要不要专门写一个只读包装类（四个方法原样转发给棋盘）挡住？

## A
不要。四个方法全是原样转发、自己不守任何不变式，这是"只转发的类"的教科书样本——在 Python 里几乎总是 Java 习惯的残留。而且它只挡手滑不挡恶意：`view._board` 一取就绕过去了。

真正起作用的是两件事：用 `typing.Protocol`（结构化子类型协议）定义一个只含读方法的 `BoardView`，把"策略只该看"写进类型签名，类型检查器会在 `view.place(...)` 上报错；以及让 `free_cells()`、`rows()` 返回**元组快照**而不是内部列表——这一条是硬的，外部拿到手的东西根本改不动棋盘。包装类真正该出场的场景是跨信任边界执行第三方代码，而那需要的是进程隔离，不是一层转发。
