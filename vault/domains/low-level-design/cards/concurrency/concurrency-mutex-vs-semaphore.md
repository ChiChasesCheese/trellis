---
id: concurrency-mutex-vs-semaphore
node: concurrency.primitives
type: qa
step: 2
---
## Q
`threading.Lock` 和 `threading.Semaphore` 分别用来解决什么问题？`BoundedSemaphore` 又比普通 `Semaphore` 多做了什么？

## A
`Lock` 是二元的（锁住/未锁住），表达"同一时刻只有一个线程能进临界区"；`Semaphore` 内部是一个计数器，表达"同一时刻最多 N 个线程能进入"——典型用法是限制并发连接数或线程池大小，比如 `Semaphore(5)` 保护一个最多支持 5 个并发连接的资源池。二者都用 `acquire()`/`release()`，都支持 `with` 语句。

`Semaphore` 的计数器可以被任何线程 `release()`（甚至是没调用过 `acquire()` 的线程），这让它也能当"信号"用；但这也是常见误用来源——多 `release()` 一次会让计数器超过设计上限而不报错。`BoundedSemaphore` 在计数器超过初始值时会抛 `ValueError`，专门用来在测试里捕获这种"释放多了"的编程错误。
