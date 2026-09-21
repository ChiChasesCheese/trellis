---
id: eq-default-identity-and-hash
node: classes.pythonic-object
type: qa
source: python-docs
---
## Q
一个类什么都不重写时，`==` 比较的是什么？重写了 `__eq__()` 却不重写 `__hash__()` 会发生什么？

## A
`object` 默认的 `__eq__()` 按身份（identity）比较，等价于 `True if x is y else NotImplemented`，因此两个字段完全相同的实例默认也判 `!=`。一旦子类重写 `__eq__()` 而不重写 `__hash__()`，解释器会把该类的 `__hash__` 隐式设为 `None`，实例变得不可哈希（不能作 `dict` 键或放进 `set`），因为「相等的对象必须有相同哈希值」这条约束不能再被保证。
