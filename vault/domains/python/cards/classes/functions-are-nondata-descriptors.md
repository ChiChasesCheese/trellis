---
id: functions-are-nondata-descriptors
node: classes.properties-descriptors
type: qa
source: python-docs
---
## Q
普通函数写在类体里，为什么通过实例访问时会自动变成「绑定方法（bound method）」，第一个参数 `self` 会被自动填上？这跟描述符协议有什么关系？

## A
函数对象本身实现了 `__get__()`（因此是非数据描述符）：当从实例上取出一个存在类字典里的函数时，触发的是函数的 `__get__(obj, objtype)`，返回一个绑定方法对象——它把原函数存进 `__func__`，把取出它的实例存进 `__self__`，调用时自动把 `__self__` 作为第一个参数传给 `__func__`。这正是「实例方法调用自动传 self」的底层机制，也是为什么方法在类字典里天然是非数据描述符而非硬编码的特殊语法。
