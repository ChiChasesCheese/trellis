---
id: python-data-model-repr-contract
node: python.data-model
type: qa
step: 6
tags: [grown]
---
## Q
`__repr__` 的设计目标是什么，为什么给自定义类补一个好的 `__repr__` 在代码评审里“买”到的东西比看起来多？

## A
`__repr__` 的目标是**无歧义、面向开发者**的表示，理想情况下 `eval(repr(obj)) == obj`（哪怕实际做不到，也要让人一眼看出对象的关键字段）。它不是你显式调用的——REPL、调试器、日志、`pytest` 的断言失败信息都会自动用它来打印对象，所以一个好的 `__repr__` 相当于免费获得了跨工具的可观测性（observability）；没有它，默认的 `<Point object at 0x7f...>` 在任何调试场景里都是噪音。
