---
id: first-class-functions-60s-pitch
node: functions.first-class
type: qa
source: python-docs
---
## Q
60 秒内讲清楚：「函数是一等对象」这件事对写 Python 代码有什么实际意义？

## A
第一，函数能像值一样传递，`sorted`/`map`/装饰器都是靠把函数当参数或返回值传递来实现的；第二，可以用闭包或「返回函数的函数」动态生成带参数的行为，不必都写成类；第三，函数对象自带 `__name__`、`__doc__` 等元数据，配合 `functools.wraps` 能在包装后依然保留可读的内省信息。
