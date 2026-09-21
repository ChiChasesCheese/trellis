---
id: comparison-vs-arithmetic-reflection-naming
node: classes.operator-overloading
type: qa
source: python-docs
---
## Q
算术运算符的反射方法要单独定义一套名字（`__add__`/`__radd__`），比较运算符（如 `<`）呢？

## A
不需要单独一套：比较运算符的六个方法（`__lt__`、`__le__`、`__eq__`、`__ne__`、`__gt__`、`__ge__`）本身两两互为彼此的反射方法，不再另设 `__rlt__` 之类的名字——`__lt__` 和 `__gt__` 互为反射，`__le__` 和 `__ge__` 互为反射，`__eq__` 和 `__ne__` 各自是自己的反射。这一点和算术运算符（`__add__` 配独立的 `__radd__`）的设计不同，是因为『小于』和『大于』本来就是同一件事换个方向看，不需要额外的方法名字。
