---
id: hl-os-head-tail-false-sharing
node: foundations.os-processes-threads-ipc
type: qa
step: 43
---
## Q
SPSC 环形缓冲里 `head` 和 `tail` 放在同一缓存行会发生什么？

## A
生产者持续写 `tail`，消费者持续写 `head`。同一缓存行里，每次写都使对方核心那一行失效，两个核反复抢这一行（伪共享），每次访问几十 ns 的跨核通信，吞吐大降。

分开放，各核独占自己的行，只在读对方序号时才传输（配合缓存对方序号，多数时候都不需要）。
