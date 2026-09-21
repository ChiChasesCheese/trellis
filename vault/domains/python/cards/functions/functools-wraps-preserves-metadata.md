---
id: functools-wraps-preserves-metadata
node: functions.decorators
type: qa
source: python-docs
---
## Q
写一个装饰器时，如果内层的 `wrapper` 函数不加 `@functools.wraps(原函数)`，外部看到的 `wrapper.__name__`、`wrapper.__doc__` 会是谁的？`wraps` 具体做了什么让这个问题消失？

## A
不加 `wraps` 时，这些都是内层 `wrapper` 自己的名字和文档字符串，而不是原函数的——因为最终绑定给外部名字的对象就是 `wrapper`。`functools.wraps(原函数)` 本质上是调用 `update_wrapper`，把原函数的 `__module__`、`__name__`、`__qualname__`、`__annotations__`、`__doc__` 等元数据复制到 `wrapper` 上，并合并 `wrapper.__dict__`，同时自动给 `wrapper` 加一个指回原函数的 `__wrapped__` 属性。
