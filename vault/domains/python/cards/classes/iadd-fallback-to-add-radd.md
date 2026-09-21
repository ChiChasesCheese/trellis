---
id: iadd-fallback-to-add-radd
node: classes.operator-overloading
type: qa
source: python-docs
---
## Q
`x += y` 在类没有定义 `__iadd__()`（或它返回 `NotImplemented`）时，退化成什么？

## A
退化为普通的 `x = x + y`，也就是按 `x + y` 的常规求值规则去试 `x.__add__(y)`，不行再试 `y.__radd__(x)`。如果类定义了 `__iadd__()`，`x += y` 等价于 `x = x.__iadd__(y)`，约定是就地修改 `self` 并返回结果（返回值不强制是 `self` 本身，但通常是）——这也是为什么可变类型（如 `list`）的 `+=` 和不可变类型（如 `tuple`）的 `+=` 行为看起来不同：前者真的原地改了，后者其实是重新构造了一个新对象再重新绑定名字。
