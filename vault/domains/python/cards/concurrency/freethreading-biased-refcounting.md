---
id: freethreading-biased-refcounting
node: concurrency.free-threading
type: qa
source: python-docs
---
## Q
自由线程构建用什么机制替代 GIL 来保证引用计数（reference counting）的线程安全，而不是给每个对象都加锁？

## A
用“偏向引用计数”（biased reference counting）：每个对象有一个“拥有线程”，该线程对这个对象的增减引用计数走无锁的快速路径；其它线程要修改同一对象的引用计数时走较慢的路径（涉及排队协调）。这样大多数引用计数操作（发生在拥有该对象的线程里）几乎和 GIL 模式一样快，只有跨线程共享的对象才付出额外同步成本，避免了给每个对象都加锁带来的普遍性能损失。
