---
id: hl-j05-statement-pain
node: java21.j05-switch-expressions
type: qa
step: 1
---
## Q
Java 8 的 `switch` 是"语句"（statement）而不是"表达式"，用它算一个值要多做哪些事？有哪三个麻烦？

## A
语句只做事，不产出值。要算值得：声明临时变量、每个分支赋值、每个分支别忘 `break`、两个标签共用分支要"故意不写 `break`"。

三个麻烦：
1. **fall-through（贯穿）**：匹配后一路往下执行直到 `break`，忘了就掉进下一分支；
2. **所有 `case` 共享一个作用域**；
3. **不强制处理所有情况**：`enum` 以后加常量，老 `switch` 默默走 `default`。

`switch` 表达式（Java 14 正式，12、13 为预览）一次解决这三点。
