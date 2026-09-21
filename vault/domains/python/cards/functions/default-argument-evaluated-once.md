---
id: default-argument-evaluated-once
node: functions.arguments
type: qa
source: python-docs
---
## Q
`def f(x, cache=[]):` 这种默认参数值（default parameter value）是在每次调用 `f()` 时求值，还是只求值一次？这一点对可变对象做默认值为什么特别危险？

## A
默认参数值在 `def` 语句执行（函数定义）时从左到右求值一次，之后每次调用都复用这个预先算好的对象，不会重新求值。如果默认值是列表、字典这类可变对象，某次调用里原地修改了它（比如 `append`），这个修改会残留到下一次调用。安全写法是把默认值写成 `None`，再在函数体内判断 `if x is None: x = []`，让每次调用都拿到全新对象。
