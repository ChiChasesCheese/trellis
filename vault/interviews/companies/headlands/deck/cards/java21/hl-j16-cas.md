---
id: hl-j16-cas
node: java21.j16-concurrency-primitives
type: qa
step: 11
---
## Q
CAS（compare-and-swap）是什么？`AtomicLong.incrementAndGet()` 的 CAS 循环怎么写？它的好处和代价是什么？

## A
CPU 提供的**原子指令**：

```
compareAndSet(addr, expected, new):
    if (*addr == expected) { *addr = new; return true; }
    else return false;       // 整个过程不可分割
```
x86 上是 `lock cmpxchg`；ARM 上是 `ldxr/stxr`（LL/SC）或 ARMv8.1 的 `cas`。`compareAndSet` 被 C2 当 intrinsic 直接编译成这些指令。

```java
long prev;
do { prev = value.get(); } while (!value.compareAndSet(prev, prev + 1));  // 失败说明别人改过，重读重试
```
好处：**无锁**（lock-free），没有线程会因别的线程被挂起而阻塞，任一时刻总有某个线程成功。代价：竞争激烈时大量重试。
