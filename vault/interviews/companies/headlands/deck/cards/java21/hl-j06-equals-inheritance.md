---
id: hl-j06-equals-inheritance
node: java21.j06-instanceof-pattern
type: qa
step: 15
---
## Q
`instanceof` 版 `equals` 在类可被继承时有什么隐患？怎么处理？哪些类没有这个问题？

## A
`Instrument` 若可被继承，`instanceof` 版 `equals` 会让**子类与父类实例可能"相等"**，破坏对称性。

处理：改用 `getClass() == o.getClass()`。

没有这个问题的：**`final` 类**和 **`record`**（`equals` 自动生成）。
