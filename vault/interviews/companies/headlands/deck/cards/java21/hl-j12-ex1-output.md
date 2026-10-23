---
id: hl-j12-ex1-output
node: java21.j12-scoped-values
type: qa
step: 13
---
## Q
`ScopedValue` 在绑定前、绑定块内、块外，`isBound()`、`get()`、`orElse` 各是什么结果？

## A
- 绑定前：`isBound=false`，`orElse("<anonymous>")` 返回默认值，`get()` 抛 `NoSuchElementException`。
- 块内：`isBound=true`，深层方法 `deep()` 直接读到 `USER=alice`，不需要参数。
- 块外：`isBound=false`，**自动回到未绑定**。

不需要 `try/finally`，对比 `ThreadLocal` 忘记 `remove()` 导致的串号。
