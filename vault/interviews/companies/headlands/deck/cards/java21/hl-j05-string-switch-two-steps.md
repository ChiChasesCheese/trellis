---
id: hl-j05-string-switch-two-steps
node: java21.j05-switch-expressions
type: qa
step: 17
---
## Q
字符串 `switch` 编译后分哪两步完成？为什么第一步之后还要 `equals`？

## A
1. 算 `hashCode()`，`lookupswitch` 找到"可能是哪个字符串"，分支里再 `equals` 确认，并把"第几个标签"存入临时 `int` 变量；
2. 对该变量做普通 `tableswitch` 跳到分支体。

要 `equals` 是因为**不同字符串可能哈希碰撞**，只凭哈希不能确定。
