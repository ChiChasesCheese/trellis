---
id: uth-kafka-timing-wheel-2-no-tick
node: kafka.timing-wheel
type: qa
step: 2
---
## Q
**时间轮不需要每毫秒滴答**｜Kafka · 4.0

最细的一层每格只有 1 ms，难道有个线程每毫秒转一格？

## A
**结构。** 不是。每个非空的格（bucket）被放进一个 `DelayQueue`，按格的到期时间排序；线程 `poll` 阻塞到最早的格到期，再把时钟直接推进到那一格的起点。

**细节。**

- `DelayQueue` 里装的是格，不是任务，元素个数不超过格数。
- 取出到期的格后 `flush`：每个任务重新 `add`，已到期的直接执行，来自高层的落进更细的层。

**为什么。** 推进时间的代价取决于非空格的个数，而不是任务总数；系统空闲时线程就睡着。

**对应 LeetCode：** LC 253 会议室 II · LC 23 合并 K 个升序链表
