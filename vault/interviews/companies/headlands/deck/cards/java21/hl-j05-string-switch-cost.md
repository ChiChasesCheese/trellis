---
id: hl-j05-string-switch-cost
node: java21.j05-switch-expressions
type: qa
step: 18
---
## Q
字符串 `switch` 的运行代价是多少，与 `if (s.equals("A")) ... else if ...` 相比如何？`null` 选择器会怎样，为什么？

## A
代价是"一次 `hashCode`（`String` 缓存哈希，通常 O(1)）+ 至多一次 `equals`"，不是逐个比较。分支多时比 `equals` 的 `if-else` 链快，分支少时差别可忽略。

`null` 选择器抛 **NPE**，因为第一步要调 `hashCode()`。
