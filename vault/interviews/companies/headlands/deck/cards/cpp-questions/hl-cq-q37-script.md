---
id: hl-cq-q37-script
node: cpp-questions.i-low-latency
type: qa
step: 11
---
## Q
用英文 60 秒回答：How does a lock-free single-producer single-consumer (SPSC) queue work?

## A
结构：2 的幂环形缓冲 + 两个单调索引 + release/acquire，无锁无 CAS → 细节：两索引分缓存行、缓存对方索引（72 到 2 ns/项，对比 mutex 队列 15–50 ns）→ 仅限一生产一消费，满/空由调用者处理。

- An SPSC queue is a **fixed-size ring buffer**, power-of-two capacity so I mask instead of modulo, with two monotonically increasing indices: `tail` written only by the producer and `head` only by the consumer. The producer writes the element, then does a **release store** on `tail`; the consumer **acquire-loads** `tail`, so it is guaranteed to see the element. No locks, no CAS.
- The performance details: put `head` and `tail` on **separate cache lines** to avoid false sharing, and **cache the other side's index** locally. In my test that took the queue from about 72 ns per item to 2 ns; a mutex-protected `std::queue` was 15 to 50 ns.
- It only works for exactly one producer and one consumer. The caller decides what to do when the queue is full or empty - spin or back off.
