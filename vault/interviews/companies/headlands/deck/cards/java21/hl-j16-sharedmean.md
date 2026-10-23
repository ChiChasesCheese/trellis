---
id: hl-j16-sharedmean
node: java21.j16-concurrency-primitives
type: qa
step: 38
---
## Q
单写者、多读者的队列均值（`SharedMean`）怎么用 `VarHandle` 发布一致快照并保证唯一写者？

## A
```java
public Stat read() { return (Stat) PUBLISHED.getAcquire(this); }
private void publish() {
    PUBLISHED.setRelease(this, new Stat(++seq, queue.size(), queue.sum()));
}
private void claimWriter() {
    Thread me = Thread.currentThread();
    Thread cur = (Thread) OWNER.getAcquire(this);
    if (cur == me) return;
    if (cur != null || !OWNER.compareAndSet(this, null, me))
        throw new IllegalStateException("single-writer violated");
}
```
- 两个 `VarHandle` 都是 `static final`。
- **发布不可变快照** `Stat(seq, size, sum)`：写者 `setRelease`，读者 `getAcquire` 读一次引用，读到的一定是某个真实时刻的一致快照，**不会读到「新 sum + 旧 size」的撕裂值**。对象构造时的所有字段写入都在 `setRelease` 之前。
- `OWNER.compareAndSet(this, null, me)`：CAS 做一次性占位，第一个写者抢到，其他线程再写抛异常。
- 用 `volatile Stat published` 也行且更简单；release/acquire 演示更弱的内存序足够（单写者只需发布顺序）。
