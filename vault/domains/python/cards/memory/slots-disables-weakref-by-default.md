---
id: slots-disables-weakref-by-default
node: memory.weakref
type: qa
source: python-docs
---
## Q
一个类定义了 `__slots__` 之后，它的实例默认还能不能被弱引用（weak reference）？

## A
默认不能。定义 `__slots__` 会关闭该类实例的弱引用支持，因为普通实例的弱引用信息本来是存在实例的 `__weakref__` 槽位里的，而 `__slots__` 不再自动创建这个槽位；如果既要用 `__slots__` 省内存，又要支持弱引用，必须在 `__slots__` 的字符串序列里显式加上 `'__weakref__'` 这一项。
