---
id: deadlock-lock-order
node: concurrency.locks-races
type: qa
source: python-docs
---
## Q
两个线程各自持有一把锁、又都在等待对方持有的另一把锁，这是什么问题？最基本的预防办法是什么？

## A
这是死锁（deadlock）：线程 A 持有锁 1 等锁 2，线程 B 持有锁 2 等锁 1，双方永远阻塞。最基本的预防办法是给所有锁定义一个全局固定的获取顺序（lock ordering），所有需要同时持有多把锁的代码都必须按这个顺序 `acquire()`，从根源上消除“互相等待对方持有的锁”的环路；此外，给 `acquire()` 加 `timeout` 并在拿不到锁时回退、释放已持有的锁重试，也能避免永久卡死。
