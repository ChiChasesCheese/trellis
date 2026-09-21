---
id: eq-notimplemented-fallback
node: classes.pythonic-object
type: qa
source: python-docs
---
## Q
`__eq__()` 在没法比较两个操作数时应该 `raise TypeError` 还是返回别的值？如果双方都表示「不知道怎么比」，`==` 最终得到什么结果？

## A
应该返回单例 `NotImplemented`（不是异常），把决定权交给解释器去试对方的反射方法。如果左右两侧的 `__eq__()` 都返回 `NotImplemented`，`==`/`!=` 会退回按 `is`/`is not` 比较，而不是抛异常——这保证任意两个对象之间 `==` 总有结果。
