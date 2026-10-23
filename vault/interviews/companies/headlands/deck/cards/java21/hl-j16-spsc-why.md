---
id: hl-j16-spsc-why
node: java21.j16-concurrency-primitives
type: qa
step: 32
---
## Q
解释 SPSC 队列里 `tail` 用 `setRelease` 写、`getAcquire` 读为什么就够了，不需要 `volatile`。

## A
- release 写保证此前的写（含槽位数据）不被重排到它之后；
- acquire 读保证此后的读不被重排到它之前；
- 所以消费者 acquire 读到新 `tail`，就**一定看到**生产者在 release 前写进槽位的数据。

队列正确性不需要「写之后的读不能越过写」（StoreLoad），所以不付 `volatile` 全栅栏的代价（x86 上尤其明显）。
