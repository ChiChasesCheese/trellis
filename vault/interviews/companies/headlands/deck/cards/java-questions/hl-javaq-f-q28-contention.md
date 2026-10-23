---
id: hl-javaq-f-q28-contention
node: java-questions.f-concurrency
type: qa
step: 11
---
## Q
8 线程竞争一个计数器各 500 万次，`synchronized`、`ReentrantLock`、`AtomicLong`、`LongAdder` 各约多少毫秒？为什么 `AtomicLong` 在高竞争下反而慢？`LongAdder` 为什么快、有什么代价？

## A
- 数据：synchronized **228 ms**、ReentrantLock **236 ms**、AtomicLong **320 ms**、LongAdder **17 ms**。
- 低竞争（1 线程）：AtomicLong 最快（6 ms vs 13 ms）。
- **高竞争下 AtomicLong 慢**：所有核反复争抢同一条缓存行，CAS 失败重试，每次重试都浪费一次缓存行传输；锁则让线程排队 / 睡眠，避免空转。
- **LongAdder 快一个数量级**：每个线程（哈希后）更新自己的 `Cell`（各占一条缓存行），只有 `sum()` 时才汇总。
- 代价：`sum()` 不是原子快照、占内存更多；适用统计计数器，不适用序列号分配这类需要精确同步判断的值。
