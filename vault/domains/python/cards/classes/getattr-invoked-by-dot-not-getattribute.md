---
id: getattr-invoked-by-dot-not-getattribute
node: classes.attribute-lookup
type: qa
source: python-docs
---
## Q
`__getattr__()` 到底是被谁调用的——是 `__getattribute__()` 内部调用它吗？这对『绕过 `__getattr__`』这件事意味着什么？

## A
不是。`__getattribute__()` 的实现里并不包含调用 `__getattr__()` 的逻辑；真正负责「`__getattribute__()` 抛出 `AttributeError` 时改叫 `__getattr__()`」的是点号运算符和内建函数 `getattr()` 自己的调用逻辑（一个 `try/except AttributeError` 包装）。这意味着如果代码显式调用 `obj.__getattribute__(name)`，或者在子类里用 `super().__getattribute__(name)` 绕过默认入口，那么即使查找失败，也不会自动退回去调用 `__getattr__()`——因为触发 `__getattr__()` 的那层包装被跳过了。
