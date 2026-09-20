---
id: oop-interface-vs-abstract-class
node: oop.interfaces
type: qa
step: 1
---
## Q
在 Python 里要不要共享一个契约，判定用 `Protocol` 还是用 `abc.ABC` 的规则是什么？各举一个机考题里的例子。

## A
- **没有共享状态、只是"看起来像什么"的能力契约** → `typing.Protocol`：`FareStrategy`、`Notifiable` 这类彼此无关的类型，只要实现同一组方法签名就能互换，不需要显式继承。
- **有共享字段，或者想给一个共用的部分实现** → `abc.ABC`：国际象棋的 `Piece` 持有 `position` 字段，留一个抽象的 `possible_moves()`，让子类补完。

经验法则：没有共享字段 → `Protocol`（更弱、更容易改口的承诺）；有共享字段或想给默认实现 → `ABC`。拿不准时先从 `Protocol` 开始。
