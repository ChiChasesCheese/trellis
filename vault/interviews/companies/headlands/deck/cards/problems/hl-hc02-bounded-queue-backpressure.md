---
id: hl-hc02-bounded-queue-backpressure
node: problems.hc02-merge-k-streams
type: qa
step: 10
---
## Q
为什么每个 source 要有自己的有界队列？背压（backpressure）下每个 source 最多被读多少个元素？

## A
阻塞队列 `BlockingQueue`：`put(x)` 满了阻塞，`take()` 空了阻塞；`offer / poll` 不阻塞，满 / 空时立刻返回 `false / null`。**有界**（`new ArrayBlockingQueue<>(capacity)`）时，生产者更快则队列满后阻塞在 `put`，被「挡住」，这就是**背压**；无界队列则消费者慢时内存无限涨。`capacity ≥ 1`，否则 `IllegalArgumentException`。

**性质**：消费者完全不动时，一个 source 最多被读 **`capacity + 1`** 次：队列里 `capacity` 个，生产者手里再拿 1 个等着放。测试会精确断言这个数。

**为什么每流一个队列**：如果共用一个容量为 `capacity` 的队列，快流 A 塞满队列，合并器要决定输出必须拿到慢流 B 的队首，于是等 B；B 的生产者想 `put` 但队列已满，阻塞。合并器等 B，B 等空位，空位只有合并器消费才有——互相等待，死锁。独立队列让合并器想读哪条就读哪条。

容量选择：太小生产者常阻塞、吞吐低；太大内存多、背压反应慢，经验几十到几千，按「每流最多预读多少」想。
