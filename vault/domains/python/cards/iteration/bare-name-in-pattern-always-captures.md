---
id: bare-name-in-pattern-always-captures
node: iteration.pattern-matching
type: qa
source: peps
---
## Q
想在 `case` 模式里比较一个枚举常量，比如 `case Click((x, y), button=LEFT):`，其中 `LEFT` 是想引用的一个已有常量，这样写会有什么陷阱？

## A
一个不带点号的裸名字（unqualified name）在模式里永远会被解释成捕获模式（capture pattern），也就是「无条件匹配并把值绑定给这个名字」，而不是去比较它和某个已有常量是否相等——`button=LEFT` 会把 button 的值直接绑定给一个新变量 `LEFT`，而不是判断它是否等于 `Button.LEFT`。要按值比较常量或枚举，必须写成带点号的限定名字，比如 `button=Button.LEFT`，避免这种歧义。
