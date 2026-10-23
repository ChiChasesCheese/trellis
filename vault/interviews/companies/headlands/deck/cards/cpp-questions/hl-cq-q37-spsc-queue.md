---
id: hl-cq-q37-spsc-queue
node: cpp-questions.i-low-latency
type: qa
step: 7
---
## Q
面试题：无锁的单生产者单消费者（SPSC）队列是怎么工作的？
How does a lock-free single-producer single-consumer (SPSC) queue work?

## A
- 固定容量（**2 的幂**，用掩码代替取模）的环形数组 + 两个**只增不减**的索引：`tail` 只有生产者写，`head` 只有消费者写。
- 生产者写完数据后用 **release** 更新 `tail`；消费者用 **acquire** 读 `tail`，保证看得到元素。没有锁，也没有 CAS。
- 性能细节：索引分别放在**不同缓存行**（避免伪共享），并**缓存对方的索引**以减少跨核缓存行传输。
- 只适用于**恰好一个**生产者和一个消费者；满 / 空时怎么办（自旋或退避）由调用者决定。
