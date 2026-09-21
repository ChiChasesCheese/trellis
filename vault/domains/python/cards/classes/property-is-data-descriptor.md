---
id: property-is-data-descriptor
node: classes.properties-descriptors
type: qa
source: python-docs
---
## Q
`property` 是不是 Python 里一种独立于描述符协议的特殊机制？为什么 `@property` 装饰出来的属性访问优先级比实例 `__dict__` 里的同名条目还高？

## A
不是独立机制：`property()` 本质是一个内置的数据描述符（data descriptor）实现，它的纯 Python 等价类会同时实现 `__get__`、`__set__`、`__delete__`，内部把调用转发给 `fget`/`fset`/`fdel` 三个函数。正因为它是数据描述符，而「数据描述符优先于实例 `__dict__`」是查找机制的固定规则，所以即使实例的 `__dict__` 里意外塞进了同名的键，`obj.x` 依然会先走 property 的 `__get__()`，而不会被实例字典里的值覆盖。
