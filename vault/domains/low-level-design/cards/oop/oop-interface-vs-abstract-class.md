---
id: oop-interface-vs-abstract-class
node: oop.interfaces
type: qa
---
## Q
Interface or abstract class — what's the decision rule? One example of each from a machine-coding problem.

## A
- **Interface**: a capability contract across otherwise-unrelated types; a class can hold many — `FareStrategy`, `Notifiable`.
- **Abstract class**: a family sharing **state and a partial implementation** — chess `Piece` holding position with abstract `possibleMoves()`.

Rule of thumb: no shared fields → interface; shared fields/protected helpers → abstract class. When torn, start with the interface — it's the weaker, easier-to-revise commitment.

## Q zh
接口还是抽象类 —— 判定规则是什么？各举一个机考题里的例子。

## A zh
- **接口**：跨越彼此无关的类型的一份能力契约；一个类可以同时持有多个 —— `FareStrategy`、`Notifiable`。
- **抽象类**：共享**状态和部分实现**的一个家族 —— 国际象棋的 `Piece` 持有位置，并留下抽象的 `possibleMoves()`。

经验法则：没有共享字段 → 接口；有共享字段或 protected 辅助方法 → 抽象类。拿不准时先从接口开始 —— 它是更弱、更容易改口的承诺。
