---
id: hl-j14-mapmulti-vs-flatmap
node: java21.j14-stream-api
type: qa
step: 10
---
## Q
`mapMulti` 和 `flatMap` 什么时候选前者？为什么？

## A
`flatMap` 要为每个输入元素**创建新 `Stream`**（哪怕 `Stream.empty()` 或单元素流也有分配和管线开销）；`mapMulti` 直接把结果推给下游，**没有中间流**。

- 选 `mapMulti`：每个输入产出**少量**（尤其 0 或 1 个）结果，或命令式循环更好写。例：从混合事件里只挑 `Trade` 并配 `instanceof` 模式。
- 选 `flatMap`：产出很多结果，或结果本来就是现成的集合/流，此时 `flatMap` 的惰性更好。

对照：`flatMap(e -> e instanceof Fill f && f.qty() > 0 ? Stream.of(f) : Stream.empty())` 与 `mapMulti` 版本结果相同。多腿订单拆腿时，有 0 条腿的订单贡献 0 个元素。
