---
id: classmethod-alternate-constructor
node: classes.pythonic-object
type: qa
source: python-docs
---
## Q
`@classmethod` 的一个典型用途是充当「备选构造器（alternate constructor）」，这是什么意思，为什么必须是 `classmethod` 而不是 `staticmethod`？

## A
备选构造器指的是像 `Point.from_tuple((1, 2))` 这样，用另一种输入形式构造实例、内部再调用 `cls(...)` 返回对象的类方法。必须用 `classmethod` 是因为方法体里要用到「当前类是谁」（`cls`）才能正确地被子类继承——子类调用 `Child.from_tuple(...)` 时 `cls` 会自动是 `Child` 而非写死的父类名，`staticmethod` 拿不到这个绑定。
