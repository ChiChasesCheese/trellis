---
id: repr-str-division-of-labor
node: model.dunder-protocols
type: qa
source: python-docs
---
## Q
`repr(obj)` 和 `str(obj)` 分别调用对象的哪个特殊方法？如果一个类只定义了 `__repr__` 没有定义 `__str__`，调用 `str(obj)` 会发生什么？

## A
`repr(obj)` 调用 `obj.__repr__()`，用于生成「官方」字符串表示，理想情况下应是能重新构造出等值对象的合法 Python 表达式，主要给调试用，要求信息完整、无歧义；`str(obj)` 调用 `obj.__str__()`，用于生成给人看的「非正式」表示，不要求是合法表达式。`object` 基类对 `__str__` 的默认实现就是调用 `__repr__()`，所以只定义了 `__repr__` 的类，`str(obj)` 会退化成和 `repr(obj)` 相同的输出。
