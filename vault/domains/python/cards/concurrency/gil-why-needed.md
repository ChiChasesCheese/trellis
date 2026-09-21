---
id: gil-why-needed
node: concurrency.gil
type: qa
source: python-docs
---
## Q
CPython 的全局解释器锁（GIL，Global Interpreter Lock）保证同一进程内同一时刻只有一个线程执行 Python 字节码，这个限制的根本原因是什么？

## A
CPython 用引用计数（reference counting）管理内存：每个对象的 `ob_refcnt` 在赋值/释放时增减。这个增减不是原子操作，多线程并发修改会产生竞态，导致计数错误、提前释放或内存泄漏。GIL 把整个解释器串行化，避免给每个对象、每个容器单独加锁，是 CPython 实现简单性和单线程性能的代价交换。
