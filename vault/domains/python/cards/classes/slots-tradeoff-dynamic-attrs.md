---
id: slots-tradeoff-dynamic-attrs
node: classes.dataclasses
type: qa
source: python-docs
---
## Q
给一个类加 `__slots__ = ('x', 'y')` 换来了什么，又失去了什么？

## A
换来的是：不再给每个实例自动生成 `__dict__` 和 `__weakref__`，显著省内存，属性查找也更快——因为 `__slots__` 里声明的每个名字会在类上生成一个数据描述符（descriptor）直接指向固定的存储槽位。失去的是：实例不能再动态添加 `__slots__` 之外的新属性（赋值会抛 `AttributeError`），除非显式把 `'__dict__'` 也塞进 `__slots__`；也不再支持弱引用（weak reference），除非显式加上 `'__weakref__'`。`@dataclass(slots=True)`（3.10 起）可以自动生成这份 `__slots__`，但已存在的 `__slots__` 会导致 `TypeError`。
