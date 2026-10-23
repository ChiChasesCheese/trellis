---
id: hl-j03-new-variant-default-quiz
node: java21.j03-pattern-switch
type: qa
step: 29
---
## Q
写了 `sealed` 层级的 `switch` 之后，团队新增了一个 `record` 实现。如果 `switch` 末尾有 `default` 会怎样？如果没有呢？

## A
- **有 `default`**：编译通过，新类型悄悄落入 `default`，没有任何提示。
- **没有 `default`**：编译失败，逼你补分支；若直接跑没重编译的旧 class，则运行时抛 `MatchException`。

这是面试里常被追问的取舍：用 `sealed` + 不写 `default`，把"漏处理新变体"变成编译期错误。
