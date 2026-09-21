---
id: subclasshook-customizes-issubclass
node: classes.abc-protocols
type: qa
source: python-docs
---
## Q
除了逐个调用 `register()`，ABC 还有什么机制可以批量地、按条件地把外部类判定为自己的子类？

## A
重写 `__subclasshook__(cls, C)`（必须写成 `classmethod`）：`issubclass(C, SomeABC)` 内部会调用它，让 ABC 自己决定 `C` 算不算自己的子类，而不必对每一个符合条件的类都手动调一次 `register()`。它可以返回 `True`（判定为子类）、`False`（判定不是，即使按默认规则本该算是）或 `NotImplemented`（交回给常规的子类检查机制继续判断）。典型用法是检查 `C.__mro__` 里有没有某个约定的方法名，从而批量识别『鸭子类型上符合接口』的类。
