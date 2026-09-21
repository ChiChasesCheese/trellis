---
id: immortal-objects-benefits
node: memory.interning-immortal
type: qa
source: cpython-internals
---
## Q
既然 `None`、`True`、小整数缓存这些对象的值本来就不会变，为什么给它们做「不朽化」（immortalize，固定引用计数不再修改）还能带来实际的性能和工程收益？举两个场景。

## A
一是多核场景：多个线程同时对同一个对象做引用计数的加减，会不断使对方 CPU 核心缓存的那条缓存行失效（cache invalidation），即使对象的值从没变过；不朽对象不再改写引用计数，就没有这种缓存失效开销，也为「每解释器一把 GIL」这类免共享全局锁的方案扫清了数据竞争（data race）障碍。二是写时复制（copy-on-write）场景：预先 fork 出多个 worker 进程时，任何一次引用计数的写操作都会触发那一页内存被复制（COW），不朽对象因为不再修改引用计数，可以继续被多个子进程真正共享同一份物理内存，省下大量内存。
