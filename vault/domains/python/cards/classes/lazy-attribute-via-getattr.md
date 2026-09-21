---
id: lazy-attribute-via-getattr
node: classes.attribute-lookup
type: qa
source: python-docs
---
## Q
为什么 `__getattr__()` 天然适合实现『惰性属性（lazy attribute）』——只在第一次被访问时才计算？

## A
因为 `__getattr__()` 只在实例 `__dict__` 里还没有这个名字时才会被调用；一旦在 `__getattr__()` 里把算出来的值顺手存进 `self.__dict__[name] = value`（或 `setattr(self, name, value)`），下次再访问同名属性时，正常查找就会先在实例 `__dict__` 里命中，`__getattr__()` 就不会再被触发，等价于「算一次、缓存住」。这正是 `functools.cached_property` 之类工具背后的思路，只是它用描述符（descriptor）实现，而不是手写 `__getattr__`。
