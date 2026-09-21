---
id: cached-property-vs-property
node: functions.functools
type: qa
source: python-docs
---
## Q
`@functools.cached_property` 和普通的 `@property` 相比，在「是否允许写属性」和「计算次数」上有什么不同？为什么用了 `__slots__` 且没声明 `__dict__` 的类通常不能用 `cached_property`？

## A
普通 `@property` 每次访问都重新执行 getter，且默认禁止直接赋值（除非另外定义 setter）；`cached_property` 只在第一次访问、且实例的 `__dict__` 里还没有同名属性时才执行一次 getter，然后把结果写进实例 `__dict__`，之后的读写都直接命中这个普通属性、不再触发计算，删除该属性可以让它重新计算。因为它依赖往实例的 `__dict__` 里写缓存值，用了 `__slots__` 又没声明 `__dict__` 槽位的类没有实例字典可写，就无法使用 `cached_property`。
