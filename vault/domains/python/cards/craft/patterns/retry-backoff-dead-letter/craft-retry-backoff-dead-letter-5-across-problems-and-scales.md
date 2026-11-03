---
id: craft-retry-backoff-dead-letter-5-across-problems-and-scales
node: craft.patterns.retry-backoff-dead-letter
type: qa
step: 5
---
## Q
**重试、退避与死信 · 通知服务、紧急广播、发布订阅、熔断器里的同一条曲线**｜模式

通知服务的重试、紧急广播的订阅者重试、发布订阅的投递、熔断器的半开探测。它们的「等多久再试」有什么共同形状？放大到服务之间的调用，重试会带来什么新问题？

## A
**要点。** 同一个形状：失败一次，把等待时间乘一个系数，封顶；成功或次数用尽时重置或放弃。熔断器里探测失败后把冷却时间乘上退避系数，也是同一个公式。

```python
# notification-service：每次失败后的等待
return min(self.base_delay * (self.multiplier ** (attempt - 1)), self.max_delay)
# api-circuit-breaker：半开探测失败后，下一次冷却更长
self._timeout = min(self._timeout * self._backoff, self._max_timeout)
# pub-sub：线性退避 + 失败策略（死信）
self._sleep(self._retry_delay * attempt)
```

**见于。** notification-service、amz-emergency-pubsub、pub-sub、api-circuit-breaker。

**不变的。** 区分暂时性与永久性错误；等待时间有封顶；次数有上限；用尽后留下记录（死信）；异常不逃出投递循环。**变化的。** 曲线（指数、线性）；等待发生的位置（延迟堆、投递线程里 `sleep`）；谁决定放弃（次数、总时长、熔断器）。

**信号。** 需求里出现「失败要重试」「不能丢消息」「第三方接口不稳定」「消息卡住了」；或者你想写 `while True: try: ... except: sleep(1)`。

**尺度对照。** 低层设计：策略对象 + 延迟堆 + 死信列表。分布式：消息队列的重投与死信队列（例如 SQS 的 redrive：消息被接收超过 `maxReceiveCount` 次后移入死信队列）；HTTP 客户端的重试加幂等键。变化：重试会**放大**流量，调用链有 3 层、每层重试 3 次，最底层一次失败可能引发最多 27 次请求，所以重试要加预算（只在入口层重试、限制重试占比），并配熔断器：对方已经倒下时，及时停止重试比耐心重试更重要。死信从内存里的一个列表变成一个需要监控、告警、人工或自动重放的队列。
