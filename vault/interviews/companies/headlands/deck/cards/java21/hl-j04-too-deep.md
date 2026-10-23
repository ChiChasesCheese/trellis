---
id: hl-j04-too-deep
node: java21.j04-record-patterns
type: qa
step: 23
---
## Q
`case A(B(C(D(var x))))` 这样的深层 record 模式有什么问题？怎么处理？绑定变量与 record 组件是什么关系？

## A
能编译，但读起来像剥洋葱。**三层以上就拆成辅助方法**，或在 `record` 上加便利访问方法。

绑定变量是组件值的**拷贝**：基本类型修改它不影响 record；引用类型拿到的是同一引用，所以浅不可变问题依然存在。
