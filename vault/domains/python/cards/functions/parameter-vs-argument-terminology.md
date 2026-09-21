---
id: parameter-vs-argument-terminology
node: functions.arguments
type: qa
source: python-docs
---
## Q
「parameter（形参）」和「argument（实参）」这两个词经常被混用，它们准确的区别是什么？

## A
parameter 是函数定义里出现的名字，规定这个函数能接受哪些种类的输入；argument 是调用这个函数时实际传进去的值。例如 `def func(foo, bar=None, **kwargs)` 里 `foo`、`bar`、`kwargs` 是 parameter；调用 `func(42, bar=314, extra=1)` 时，`42`、`314`、`1` 才是 argument。
