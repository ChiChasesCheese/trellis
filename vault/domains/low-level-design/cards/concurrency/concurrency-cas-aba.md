---
id: concurrency-cas-aba
node: concurrency.primitives
type: qa
---
## Q
一个无锁栈用 `compareAndSet(top, A, A.next)` 来出栈。CAS 成功了 —— 栈却被搞坏了。发生了什么，怎么修？

## A
**ABA 问题**：在读到 `top == A` 和执行 CAS 之间，另一个线程弹出了 A、弹出了 B，又把 A 压了回来（或者把一个*回收复用*的节点放在了 A 的地址上）。CAS 看到"还是 A"于是成功，但此时 `A.next` 指向的节点已经不在栈里了。

- 修法：给指针配一个每次更新都递增的**版本戳**（`AtomicStampedReference`、tagged pointer）—— 过期的版本会让 CAS 失败。
- 在带 GC 的语言里，经典的节点复用变体较少见（可达的 A 不会被重新分配），但值层面的逻辑 ABA 照样咬人。
