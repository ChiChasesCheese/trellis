---
id: hl-cq-cs16-ub
node: cpp-questions.cheatsheet
type: qa
step: 16
---
## Q
一句话背诵：常见未定义行为清单，以及 `x + 1 > x` 在 `INT_MAX` 上的表现。

## A
- UB：有符号溢出、越界、悬空、未初始化、移位 ≥ 位宽、数据竞争、缺 `return`。
- 例：`x + 1 > x` 在 `INT_MAX` 上，`-O0` 得 **0**，`-O2` 得 **1**。
- 无符号溢出有定义（回绕）。
