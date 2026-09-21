---
id: function-object-introspection-attrs
node: functions.first-class
type: qa
source: python-docs
---
## Q
函数对象上的 `__name__`、`__doc__`、`__defaults__` 分别保存什么？装饰器（decorator）为什么要小心保留它们？

## A
`__name__` 是定义时的函数名，`__doc__` 是文档字符串（docstring），`__defaults__` 是位置参数默认值组成的元组。用装饰器包装函数后若不处理，调用方看到的是包装函数（wrapper）自己的这些属性而不是原函数的，导致 `help()`、日志、调试器显示的名字和文档失真——这正是 `functools.wraps` 要解决的问题。
