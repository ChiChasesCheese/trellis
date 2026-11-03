---
id: craft-backpressure-overflow-policy-5-across-problems-and-scales
node: craft.patterns.backpressure-overflow-policy
type: qa
step: 5
---
## Q
**反压与溢出策略 · 循环队列、阻塞队列、线程池、日志、消息主题里的同一个「满」**｜模式

Design Circular Queue、有界阻塞队列、线程池的提交队列、异步日志、发布订阅。它们面对的都是「满了」，各自选了哪个答案？放大到跨机器的系统，反压怎么传播？

## A
**要点。** 每个有界缓冲区在满的那一刻必须选一个答案：拒绝、阻塞、丢旧。同一个接口里可以并存：`put_nowait` 是拒绝，`put(timeout=None)` 是阻塞，`put(timeout=t)` 是限时阻塞。

```python
# LeetCode Design Circular Queue：满了 enQueue 返回 False（拒绝）
def enQueue(self, value): 
    if self.size == self.cap: return False
# bounded-blocking-queue：满了阻塞，直到有空位、超时或关闭
while len(self._items) >= self._capacity and not self._closed: self._wait_for(self._not_full, ...)
# thread-pool：提交队列用信号量做准入
self._admission = threading.Semaphore(queue_capacity) if queue_capacity else None
# pub-sub：策略是枚举，由主题自己选
class OverflowPolicy(Enum): DROP_OLDEST; BLOCK; REJECT
```

**见于。** design-circular-queue、pub-sub、thread-pool、logger、amz-emergency-pubsub、bounded-blocking-queue。

**不变的。** 缓冲区一定有上限；满了的行为是显式的策略；丢弃一定留下计数或死信；阻塞一定有超时和被关闭唤醒的出口。**变化的。** 谁来承受代价（生产者、消费者、被丢掉的数据），以及丢哪一条（最老、最不重要）。

**信号。** 需求里出现「生产者比消费者快」「队列」「缓冲」「峰值流量」「消息不能丢 / 可以丢」；或者你写下了一个 `queue.Queue()` 没有 `maxsize`。

**尺度对照。** 力扣：固定大小环形缓冲区，满了返回 False。低层设计：条件变量上的阻塞、超时、关闭。分布式：TCP 的接收窗口让发送方慢下来（阻塞型反压）；Kafka 生产者缓冲区满时 `send` 最多阻塞 `max.block.ms`，之后抛错（限时阻塞）；HTTP 服务返回 429 或 503 做负载卸载（拒绝型）；监控管线丢采样（丢弃型）。变化：单机里「阻塞」只卡住一个线程；跨机器时反压要一层层传回源头，每一层的缓冲区都有上限和自己的策略，只要有一层无界，反压就会在那里被吞掉，压力变成那一层的内存。
