---
id: getattr-vs-getattribute-trigger
node: classes.attribute-lookup
type: qa
source: python-docs
---
## Q
`__getattr__()` 和 `__getattribute__()` 都能拦截属性访问，但触发条件完全不同——分别是什么？

## A
`__getattribute__()` 是无条件调用的：只要发生 `obj.x` 这样的属性访问（不论最终有没有找到），Python 都先调用它，它负责实现刚才的整条查找逻辑。`__getattr__()` 只在「正常查找失败」时才被调用——具体是 `__getattribute__()` 抛出 `AttributeError`（比如属性既不在实例 `__dict__` 也不在类树里），或者某个属性是描述符且它的 `__get__()` 抛出了 `AttributeError`。如果属性能被正常机制找到，`__getattr__()` 根本不会被调用，这是它和 `__setattr__()`（每次赋值都会被调用）刻意设计的不对称之处。
