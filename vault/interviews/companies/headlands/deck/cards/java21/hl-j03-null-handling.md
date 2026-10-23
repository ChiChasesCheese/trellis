---
id: hl-j03-null-handling
node: java21.j03-pattern-switch
type: qa
step: 4
---
## Q
`switch (o)` 里 `o == null` 时分别发生什么：(a) 无 `case null` 无 `default`；(b) 有 `default` 无 `case null`；(c) 有 `case null, default`？

## A
- (a) 抛 **`NullPointerException`**（兼容旧行为）。
- (b) 也抛 `NullPointerException`：**`default` 不处理 `null`**，不会落进 `default`。
- (c) 进入 `case null, default` 分支，不抛异常。

写了 `case null` 就由你处理；可与 `default` 合并成 `case null, default -> "other/null"`。
