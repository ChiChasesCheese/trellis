---
id: binary-op-return-notimplemented-not-raise
node: classes.operator-overloading
type: qa
source: python-docs
---
## Q
`__add__()` 这类实现二元运算符的方法，遇到不支持的操作数类型时应该 `raise TypeError` 还是返回什么？

## A
应该返回单例 `NotImplemented`，而不是自己抛异常。这样解释器才有机会去尝试对方的反射方法（比如 `x + y` 里 `x.__add__` 返回 `NotImplemented` 后，会去试 `y.__radd__`）；只有双方都返回 `NotImplemented`（或都没定义相应方法），Python 才会最终抛出 `TypeError: unsupported operand type(s)`。如果 `__add__()` 自己直接 `raise`，就剥夺了对方类型参与运算的机会，也破坏了「双方协商」的协议。
