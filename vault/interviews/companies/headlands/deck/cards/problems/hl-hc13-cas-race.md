---
id: hl-hc13-cas-race
node: problems.hc13-fixed-memory-pool
type: qa
step: 9
---
## Q
并发里的竞争条件、CAS（compare-and-set）和 lock-free / wait-free 分别是什么？最简单的线程安全版本怎么写？

## A
并发正确性要考虑：**原子性**、**可见性**（写入何时被别的线程看到）、**有序性**（编译器和 CPU 可能重排）。`VarHandle`（Java 9）是对字段做精确内存操作（指定内存序的读写、CAS）的句柄。

**竞争条件**：两线程都「读 head → 改 head」，交错就丢更新：线程 1 读 `head=5`，线程 2 读 `head=5` 并写 `head=next[5]`，线程 1 再写 `head=next[5]`——两个线程都借走了块 5。

**CAS**：`CAS(变量, 期望值, 新值)`——**原子地**检查变量是否为期望值，是就改成新值并返回 true，否则什么也不做返回 false；失败的线程重读重试。是无锁算法的基石。

**lock-free vs wait-free**：lock-free 保证系统整体总有线程在前进，单个线程可能一直 CAS 失败；wait-free 每个线程在有限步内完成。池里的 CAS 重试循环是 lock-free。无锁 ≠ 无等待。无锁真正的卖点是不会被挂起的线程拖住别人（无优先级反转），不是吞吐。

**最简单的正确解：加锁**（面试先说这个）：
```java
class LockedPool {
    private final GenPool pool; private final ReentrantLock lock = new ReentrantLock();
    long allocate() { lock.lock(); try { return pool.allocate(); } finally { lock.unlock(); } }
    FreeResult free(long h) { lock.lock(); try { return pool.free(h); } finally { lock.unlock(); } }
}
```
用 `ReentrantLock` 而非 `synchronized`：JDK 21 里虚拟线程在 `synchronized` 内阻塞会钉住载体线程。问题只是所有线程排队过同一把锁。

`volatile int head` 只解决可见性，不解决 ABA（「值相同但历史不同」）。`Thread.onSpinWait()` 提示 CPU 在自旋，可省电 / 让出超线程资源。`compare_exchange_weak` 在 C++ 里可能无竞争也失败，必须放循环里；`strong` 只在真不相等时失败。
