---
id: hl-j02-command-event
node: java21.j02-sealed
type: qa
step: 16
---
## Q
订单引擎里怎么用两棵 `sealed` 层级建模命令（Command）和事件（Event）？这样设计有什么好处？

## A
```java
sealed interface Command permits Limit, Cancel { long id(); }   // 接口里可放所有变体共有的方法
record Limit(long id, Side side, long px, long qty) implements Command {}
record Cancel(long id) implements Command {}

sealed interface Event permits Rested, Cancelled, Rejected {}
```
输入（命令）一棵、输出（事件）一棵。`execute(Command)` 是唯一入口，所有按命令种类分派集中在一处 `switch`；`render(Event)` 是唯一出口。

好处：以后加一种命令，编译器逼你补全所有分派点。完整订单簿的结构是 `Command permits Limit, Market, Cancel, Modify`、`Event permits Trade, Rested, Cancelled, Modified, Rejected`。
