---
id: qsbr-lock-free-reclamation
node: concurrency.free-threading
type: qa
source: python-docs
---
## Q
自由线程构建里的 QSBR（Quiescent-State Based Reclamation，静止状态回收）解决的是什么问题？

## A
对 `dict`/`list` 这类支持无锁并发读的容器，当它们扩容替换掉内部数组时，不能立刻释放旧数组的内存——因为可能还有别的线程正在并发读取这块内存，立刻释放会造成 use-after-free。QSBR 要求每个线程周期性地报告自己处于“静止状态”（quiescent state，即当前没有持有任何可能被回收的共享对象引用），只有当所有线程都已报告经过了某次回收请求之后的静止点，才真正释放被替换下来的旧内存；这样既避免了用锁保护每次读取带来的开销，又保证了内存安全，代价是内存的实际释放会被推迟。
