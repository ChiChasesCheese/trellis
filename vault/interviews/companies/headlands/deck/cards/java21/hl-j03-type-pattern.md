---
id: hl-j03-type-pattern
node: java21.j03-pattern-switch
type: qa
step: 2
---
## Q
`case Integer i ->` 里的"类型模式"（type pattern）和"绑定变量"（binding variable）各指什么？它们的作用域、分支匹配顺序和选择器类型有什么规则？

## A
`case Integer i`：**若选择器是 `Integer`，就绑定到新变量 `i`（类型 `Integer`）并执行该分支**，已经转好型。`Integer i` 是类型模式，`i` 是绑定变量。

- 绑定变量只在**本分支**可见，不同分支可重名。
- `switch (o)` 的 `o` 叫**选择器**（selector），Java 21 里用模式的 `switch`，选择器必须是**引用类型**。
- 分支**从上到下依次尝试，第一个匹配的生效**。
