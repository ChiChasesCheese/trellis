---
id: repr-reconstructs-object
node: classes.pythonic-object
type: qa
source: python-docs
---
## Q
为什么惯例上建议 `__repr__()` 的返回值「尽可能」是一段能重建同值对象的合法 Python 表达式，而不是像 `__str__()` 那样只求可读？

## A
`__repr__()` 面向调试和日志，要求信息完整、无歧义：官方文档规定它应尽量返回可用来重新创建等值对象的表达式（如 `Point(x=1, y=2)`），做不到时退化为 `<...说明...>` 形式。`__str__()` 面向最终用户，只求简洁易读，没有「可求值」的要求。若类只定义了 `__repr__()` 没定义 `__str__()`，`str()` 和 `print()` 会退回用 `__repr__()` 的结果。
