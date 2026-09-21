---
id: radd-dispatch-conditions
node: classes.operator-overloading
type: qa
source: python-docs
---
## Q
`x + y` 求值时，什么情况下解释器会去调用 `y` 的 `__radd__()`，而不是只用 `x` 的 `__add__()`？

## A
有两种情况会触发反射方法（reflected method）`type(y).__radd__(y, x)`：一是 `type(x).__add__(x, y)` 返回了 `NotImplemented`（`x` 自己说「不会处理和 `y` 的加法」）；二是 `type(y)` 是 `type(x)` 的子类，且它重写了 `__radd__()`——这时哪怕 `x.__add__()` 能正常处理，也会优先调用 `y` 的反射方法，让子类有机会覆盖祖先类的运算行为。第一种情况的前提是双方类型不同；两者类型相同时不会去试反射方法。
