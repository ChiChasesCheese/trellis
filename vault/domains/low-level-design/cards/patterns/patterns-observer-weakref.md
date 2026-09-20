---
id: patterns-observer-weakref
node: patterns.observer
type: qa
step: 2
---
## Q
为什么 Observer 的订阅列表容易造成内存泄漏，`weakref` 怎么帮上忙？

## A
subject 通常比订阅者活得久（比如一个长期存在的事件总线）；如果它用普通列表强引用每一个订阅者，订阅者对象即使已经没有别处再用，也不会被垃圾回收——这是一种隐藏的内存泄漏。改用 `weakref.WeakSet` 持有订阅者，订阅者被别处释放后会自动从列表里消失，不需要显式调用 `unsubscribe()`。代价是：如果订阅者只是一个临时创建、没有别处持有的闭包或 lambda，弱引用会让它立刻被回收，回调再也不会触发——所以只对"确实有其他地方持有"的对象用弱引用。
