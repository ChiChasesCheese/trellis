---
id: hl-j16-condition-code
node: java21.j16-concurrency-primitives
type: qa
step: 35
---
## Q
用 `ReentrantLock` + `Condition` 写有界缓冲的 `put`。为什么等待要用 `while` 而不是 `if`？

## A
```java
void put(T x) throws InterruptedException {
    lock.lockInterruptibly();
    try {
        while (count == items.length) notFull.await();   // 用 while 不用 if
        items[putIdx] = x; /* 更新索引与 count */
        notEmpty.signal();
    } finally { lock.unlock(); }
}
```
用 `while` 是为了防**虚假唤醒**（spurious wakeup）：被唤醒后条件可能仍不成立，必须重新检查。实验：容量 4 传 1..1000，和 = 500500。

生产者消费者跑在虚拟线程上，`await()` 时被卸载，不占载体。另一线程 `tryLock(100ms)` 拿不到锁返回 false，放弃而不是死等。
