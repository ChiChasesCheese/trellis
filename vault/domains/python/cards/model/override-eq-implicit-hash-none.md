---
id: override-eq-implicit-hash-none
node: model.hash-eq
type: qa
source: python-docs
---
## Q
一个类只重写了 `__eq__` 却没有重写 `__hash__`，它的实例还能不能放进 set 或者当字典键？

## A
不能。用户定义的类默认从 `object` 继承 `__eq__` 和 `__hash__`（按身份比较、身份哈希），但只要类重写了 `__eq__` 而没有显式定义 `__hash__`，解释器会把该类的 `__hash__` 隐式设为 `None`；此时对该实例调用 `hash()` 会抛出 `TypeError`，`isinstance(obj, collections.abc.Hashable)` 也会正确返回 False，也就不能作为 set 元素或字典键。
