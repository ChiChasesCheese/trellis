---
id: test-mock-where-to-patch
node: engineering.testing
type: qa
source: python-docs
---
## Q
模块 `b.py` 写了 `from a import SomeClass` 并在 `some_function` 里用 `SomeClass(...)`。用 `unittest.mock.patch()` 打桩 `SomeClass` 时，应该 `@patch('a.SomeClass')` 还是 `@patch('b.SomeClass')`？为什么？

## A
应该打 `@patch('b.SomeClass')`。`patch()` 替换的是「某个名字指向的对象」，而不是对象本身，同一个类可以被多个名字引用。`b.py` 用 `from a import SomeClass` 之后，`b` 模块的命名空间里已经有了自己指向 `SomeClass` 的名字，`some_function` 实际查找（look up）的是 `b.SomeClass` 这个名字，而不是 `a.SomeClass`；打桩 `a.SomeClass` 不会影响 `b` 里已经导入的那个引用。原则是：在「使用/查找对象的地方」打桩，而不是在「定义对象的地方」打桩。
