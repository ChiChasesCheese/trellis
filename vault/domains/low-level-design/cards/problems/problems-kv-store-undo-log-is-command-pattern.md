---
id: problems-kv-store-undo-log-is-command-pattern
node: problems.components.kv-store
type: qa
step: 6
tags: [grown]
---
## Q
内存键值存储的撤销日志把每一条“如何撤销一次改动”记成一个闭包（`Callable[[], None]`），而不是显式定义一个 `Command`/`UndoCommand` 类再实例化。这在设计模式的意义上属于什么，为什么在 Python 里不需要专门的类？

## A
这本质上就是命令模式（Command）——“一个可以之后再执行的动作”被封装成一个可以传递、可以入栈、可以延迟调用的对象。区别只在于用什么承载这个动作：Java 风格的做法通常需要一个带 `execute()` 方法的类，因为 Java 的函数不是一等公民；Python 的函数（包括闭包）本身就是可以被传递、存进列表、之后调用的对象，一个 `lambda` 已经完整具备“一个可撤销动作”所需要的一切，专门再定义一个只有一个方法的类只是多一层没有增加信息的包装。
