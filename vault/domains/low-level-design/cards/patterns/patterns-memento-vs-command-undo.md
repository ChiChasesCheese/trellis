---
id: patterns-memento-vs-command-undo
node: patterns.command
type: qa
step: 3
---
## Q
Command 和 Memento 都能用来实现撤销（undo），在同一个系统里它们各自该负责什么？

## A
Command 存储**调用本身**——操作加上它的逆操作（`cmd.execute()` / `cmd.undo()`）。优点是紧凑、单一职责；缺点是每个命令都要自己想清楚怎么撤销，逻辑分散、复杂操作容易漏掉某个副作用。Memento 存储**完整的状态快照**，撤销就是把状态整个换回去，通用但内存开销更大、状态越大越慢。

常见分工：简单操作、逆操作显而易见时用 Command；状态复杂、必须保证撤销绝对可靠时用 Memento；混合做法是让 Command 记录"做了什么"，需要的关键节点再用 Memento 存一份检查点。
