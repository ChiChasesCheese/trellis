---
id: hl-javaq-f-q28-say60
node: java-questions.f-concurrency
type: qa
step: 33
---
## Q
用英文 60 秒回答：What is CAS? How do atomics work? Is lock-free always faster than locking? What is `LongAdder`?

## A
结构：CAS 定义与重试循环 → 无锁不一定快（8 线程下 320 ms 对 228 ms）→ LongAdder 分条（17 ms）及其代价 → ABA → 热路径偏好单写者加队列。

> "CAS is an atomic instruction that writes a new value only if the current value still equals the expected one; atomics retry it in a loop. It's lock-free but not automatically faster. In my test with eight threads hammering one counter, `AtomicLong` took 320 ms, slightly slower than `synchronized` at 228 ms, because every failed CAS bounces the cache line between cores. `LongAdder` took 17 ms because it stripes the counter across cells, one per thread roughly, and sums on read. The trade-offs are that `sum()` isn't an atomic snapshot and you can't use it for sequence numbers. Also watch for ABA, which needs a version stamp or immutable nodes. For hot paths I prefer single-writer designs with queues over clever lock-free structures."
