---
id: lessram-slots-inheritance-gotcha
node: performance.less-ram
type: qa
source: python-docs
---
## Q
子类声明了 `__slots__`，但它的父类没有声明 `__slots__`，子类实例还能省下 `__dict__` 的内存吗？

## A
不能。只要继承链上有一个祖先类没声明 `__slots__`，实例仍然会自动带上 `__dict__` 和 `__weakref__`，子类自己的 `__slots__` 声明形同虚设——要真正省内存，必须从最顶层的基类开始每一层都声明 `__slots__`。
