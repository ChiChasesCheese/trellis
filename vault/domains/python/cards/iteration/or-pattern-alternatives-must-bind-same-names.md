---
id: or-pattern-alternatives-must-bind-same-names
node: iteration.pattern-matching
type: qa
source: peps
---
## Q
用 `|` 写 or 模式（or pattern）组合多个分支时，比如 `[1, x] | [2, y]`，为什么这样写不合法？

## A
or 模式要求所有分支绑定完全相同的一组变量名，因为匹配成功后分支代码只能看到一套确定的变量绑定——如果分支各自绑定不同名字，就无法确定匹配成功后到底哪个名字会被赋值。`[1, x] | [2, x]` 是合法的，因为两个分支都绑定同一个名字 `x`；`[1, x] | [2, y]` 因为 `x` 和 `y` 不一致就会被拒绝。
