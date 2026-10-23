---
id: hl-j03-guard-side-effects
node: java21.j03-pattern-switch
type: qa
step: 22
---
## Q
`switch` 模式匹配的守卫里为什么不能有副作用？守卫引用外部局部变量有什么要求？

## A
守卫在类型匹配之后求值，**每次尝试都求一次**。在守卫里做副作用（改变量、读流、计数），一旦分支顺序变了行为就变，而且重复求值会重复触发副作用。

守卫引用的外部局部变量必须 **final 或 effectively final**，否则报 `local variables referenced from a guard must be final or effectively final`。
