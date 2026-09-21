---
id: freethreading-deferred-refcounting
node: concurrency.free-threading
type: qa
source: python-docs
---
## Q
自由线程构建里，模块对象（module object）等类型启用“延迟引用计数”（deferred reference counting）后，回收时机和默认构建相比有什么不同？

## A
默认构建下，对象引用计数归零就立即释放。开启延迟引用计数的对象类型（模块对象、模块顶层函数、类作用域方法、描述符、`threading.local` 对象）不对来自 Python 函数调用栈的引用计数，因此这些引用不会让计数产生频繁的跨线程更新；代价是引用计数不再能反映真实存活状态，这些对象不会在计数归零时立刻释放，而是等下一次垃圾回收（GC）扫描确认没有栈引用后才被释放——回收责任从引用计数转移给了 GC。
