---
id: match-is-not-a-switch-statement
node: iteration.pattern-matching
type: qa
source: peps
---
## Q
Python 3.10 的 `match`/`case` 和 C 语言那种只比较单一标量值的 `switch` 语句相比，本质区别是什么？

## A
`switch` 只是把值和一串常量做相等比较、跳到对应分支。`match` 的每个 `case` 后面跟的是一个模式（pattern），它同时做两件事：验证 subject（`match` 后面的值）有没有某种结构（比如是不是恰好两个元素的序列、是不是某个类的实例），并且把结构里的组成部分绑定（bind）到新名字上供分支代码直接使用。所以 `match` 能一步做完「类型/结构检查 + 解构 + 命名」，而不只是值比较。
