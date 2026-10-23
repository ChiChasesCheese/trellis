---
id: hl-j04-duplicate-names
node: java21.j04-record-patterns
type: qa
step: 20
---
## Q
同一个 `case` 里的 record 模式绑定变量名有什么限制？

## A
同一个 `case` 里所有绑定变量名**必须不同**，`Add(var l, var l)` 编译错误；也**不能与外层局部变量重名**。

不同 `case` 之间的绑定变量可以重名，因为作用域只在各自分支内。
