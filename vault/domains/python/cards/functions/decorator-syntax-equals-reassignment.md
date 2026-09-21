---
id: decorator-syntax-equals-reassignment
node: functions.decorators
type: qa
source: python-docs
---
## Q
`@d` 装饰一个函数定义为什么等价于 `f = d(f)`？这一步是在模块被导入、`def` 语句执行时发生，还是每次调用 `f()` 时才发生？

## A
`@d` 加 `def f(...): ...` 是 `def f(...): ...` 后紧跟 `f = d(f)` 的语法糖：Python 先按正常流程创建函数对象 `f`，再把它传给装饰器 `d` 调用一次，把返回值重新绑定回名字 `f`。这一步发生在 `def` 语句被执行的那一刻——对模块顶层定义的函数来说就是模块被导入（import）时，只执行一次，跟之后 `f` 被调用多少次无关。
