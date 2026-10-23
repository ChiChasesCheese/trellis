---
id: hl-j05-enum-matchexception
node: java21.j05-switch-expressions
type: qa
step: 15
---
## Q
`enum` 的 `switch` 表达式没写 `default` 时，编译器生成的 default 目标是什么？什么条件下会触发？怎么复现？

## A
default 目标抛 **`MatchException`**（更早版本抛 `IncompatibleClassChangeError`）。正常走不到。

触发条件：枚举在**编译之后**新增了常量，而 `switch` 没重编译。

复现：先编译 `RED, GREEN` 的枚举和列全它们的 `switch` 表达式，再把枚举改成 `RED, GREEN, BLUE` **只重编枚举**，传入 `BLUE` → `MatchException`。
