---
id: hl-j05-null-selector
node: java21.j05-switch-expressions
type: qa
step: 26
---
## Q
字符串、枚举、包装类型作 `switch` 选择器，值为 `null` 时会怎样？怎么处理？

## A
抛 **`NullPointerException`**，除非写了 `case null`（Java 21 起）。

字符串选择器的 NPE 来自第一步要调 `hashCode()`。要同时处理 `null` 和默认情况，写 `case null, default -> ...`。
