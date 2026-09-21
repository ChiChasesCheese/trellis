---
id: missing-wraps-failure-mode
node: functions.decorators
type: qa
source: python-docs
---
## Q
装饰器没有保留原函数的元数据，会对调试和排查问题造成什么实际影响？`__wrapped__` 属性能帮上什么忙？

## A
`help()`、日志、调试器、文档工具看到的函数名和文档字符串都变成了 `wrapper`（或 `None`），很难判断这个可调用对象到底装饰了谁；如果按函数名做缓存或路由（比如按 `__name__` 生成 key）的另一层装饰器叠上来，也可能因为名字失真而出错。`functools.wraps` 自动添加的 `__wrapped__` 属性指向最原始的函数，可以用来做内省，或者绕过某一层装饰器直接调用原始逻辑。
