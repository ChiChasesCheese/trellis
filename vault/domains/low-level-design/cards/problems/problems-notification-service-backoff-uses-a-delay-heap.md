---
id: problems-notification-service-backoff-uses-a-delay-heap
node: problems.components.notification-service
type: qa
step: 7
tags: [grown]
---
## Q
通知服务的重试退避，为什么不能在工作线程里 `time.sleep(delay)`？正确的结构是什么？存元组进 `heapq` 时有一个必须加的字段，是什么？

## A
`time.sleep` 有两个问题：这条线程睡着的时候**什么都干不了**，队列里的验证码只能等着；而且测试要验证『退避了 8 秒』就只能真的睡 8 秒。退避表达的是『什么时候可以再试』，那是一个**到期时间**，不是一次睡眠。

正确结构是一个按到期时间排序的**延迟堆**：瞬时失败时把信封的尝试次数加一压进 `heapq`，键是 `clock() + delay`；派发循环每轮先把到期的搬回主队列，再取一条来发。时钟注入之后，『到点了没有』是一次比较，于是测试推时钟就能断言退避时长和第几次进死信。

必须加的是一个**递增序号**做平局裁决：

```python
heapq.heappush(self._delayed, (due_at, next(self._tick), envelope))
```

没有它，两条同一时刻到期的记录会去比较 `Envelope`，而冻结 dataclass 默认不可比较，直接抛 `TypeError`。
