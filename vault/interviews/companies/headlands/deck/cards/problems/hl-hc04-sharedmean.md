---
id: hl-hc04-sharedmean
node: problems.hc04-queue-mean-snapshot
type: qa
step: 13
---
## Q
`SharedMean` 怎么用不可变快照 + `VarHandle` 的 release/acquire 实现无锁读？为什么正确，单写者怎么强制？

## A
```java
record Stat(long seq, int size, I128 sum) {}   // 全部 final
// 写者
queue.push(x);
PUBLISHED.setRelease(this, new Stat(++seq, queue.size(), queue.sum()));
// 读者
Stat st = (Stat) PUBLISHED.getAcquire(this);
```
**为什么正确**：`Stat` 不可变；`setRelease` 保证「构造 Stat 的所有写入」先于「引用被别人看到」，`getAcquire` 读到引用就看得到。读者要么看到旧要么新 Stat，永不半新半旧；`seq` 每次 +1，单个读者看到的 `seq` 单调不减。`Optional<Mean> mean()` 在空队列返回 `Optional.empty()`。

**单写者强制**：`push/pop` 用 `compareAndSet(this, null, me)` 抢占 `owner`（原子地「当前是 null 就设成我」），别的线程写抛 `IllegalStateException`。`queue` 和 `seq` 只有写者碰，不需同步；`published` 是普通字段，只通过 `VarHandle` 访问，只付 release/acquire 的代价，final 字段还有安全发布。

**代价**：写者每次分配一个 `Stat`（约 32 字节）；每秒百万次写时可每 N 次或每 1 ms 发布一次。`Stat` 若改成可变对象再重新发布，读者可能拿到正在被修改的同一个对象，撕裂读，不可变性保证没了。

**发布写法对比**：`synchronized`（读者排队）→ `volatile`（够用，有全序屏障）→ `VarHandle setRelease/getAcquire`（更弱更便宜，更难推理；说不清为何需要比 volatile 更弱时就用 volatile）→ `StampedLock.tryOptimisticRead`（读完校验 stamp，失败重读，适合写少读多）。
