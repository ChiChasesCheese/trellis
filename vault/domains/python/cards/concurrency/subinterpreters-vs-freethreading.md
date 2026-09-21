---
id: subinterpreters-vs-freethreading
node: concurrency.free-threading
type: qa
source: python-docs
---
## Q
子解释器（sub-interpreters，PEP 734，`concurrent.interpreters` 模块）和自由线程分别用什么方式实现多核并行，两者的隔离程度有什么区别？

## A
自由线程是在同一个解释器内关闭 GIL，让多个线程共享同一份对象、同一个命名空间，靠更细粒度的锁保证安全。子解释器自 3.12 起每个解释器拥有自己独立的 GIL，彼此运行时状态基本隔离（不共享可变对象），因此多个线程各自切换到不同子解释器运行就能获得真正的多核并行，隔离程度更接近多进程但仍在同一进程内、效率更接近线程；子解释器间的数据交换需要显式的消息传递机制（如 `concurrent.interpreters.create_queue()` 提供的跨解释器队列），而不是直接共享内存。
