---
id: hl-c13-spsc-design
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 11
---
## Q
面试问：设计一个无锁 SPSC（单生产者单消费者）环形队列。为什么不需要 CAS？
Interview question: Design a lock-free SPSC queue. Why no CAS?

## A
- `tail` 只由生产者写，`head` 只由消费者写：**没有竞争的写者**，所以不需要 CAS。
- 生产者：写槽位，再用 **release** 更新 `tail`（发布）；消费者用 **acquire** 读 `tail`，保证看到槽位内容。反之消费者 release 更新 `head`，生产者 acquire 读它以知道槽位已空。
- 容量取 **2 的幂**，用 `& (N-1)` 代替取模；计数器单调递增（无符号回绕无问题），`tail - head` 即元素数。
- `head_`、`tail_`、缓冲区各放独立缓存行（`alignas(64)`），避免伪共享。
- 满/空判断：满 `t - head == N`，空 `h == tail`。
