---
id: abc-mixin-minimal-methods
node: classes.abc-protocols
type: qa
source: python-docs
---
## Q
继承 `collections.abc.Set` 作为 mixin 时，一个类最少要实现几个方法就能自动获得 `__and__`、`__or__`、`isdisjoint` 等一整套集合运算？

## A
只需要实现 3 个抽象方法：`__contains__`、`__iter__`、`__len__`。`Set` ABC 会基于这三个方法自动提供其余的比较运算符（`__le__`、`__lt__`、`__eq__` 等）和集合运算符（`__and__`、`__or__`、`__sub__`、`__xor__` 等）作为 mixin 方法。这正是抽象基类的核心价值：只要求实现类最本质的几个方法，剩下能从这几个方法推导出来的行为全部免费获得，不用每个自定义容器类都重新实现一遍集合代数。
