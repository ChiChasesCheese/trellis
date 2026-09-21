---
id: data-vs-nondata-descriptor-priority
node: classes.properties-descriptors
type: qa
source: python-docs
---
## Q
数据描述符（data descriptor）和非数据描述符（non-data descriptor）是怎么定义的？两者在和实例 `__dict__` 冲突时谁赢？

## A
只定义了 `__get__()` 的是非数据描述符；额外定义了 `__set__()` 或 `__delete__()`（哪怕 `__set__` 里只是 `raise AttributeError` 占位）的就是数据描述符。冲突规则：如果实例的 `__dict__` 里有同名条目，数据描述符仍然赢（`obj.x` 走描述符，不走实例字典）；非数据描述符则相反，实例字典里的同名条目会盖过它。这也是为什么想造一个「只读」的数据描述符，只需定义 `__set__()` 并在里面抛 `AttributeError` 即可，不需要真的支持赋值。
