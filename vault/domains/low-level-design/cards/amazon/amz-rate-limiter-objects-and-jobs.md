---
id: amz-rate-limiter-objects-and-jobs
node: amazon.amz-rate-limiter
type: qa
step: 2
tags: [grown]
---
## Q
在限流器设计里应该有哪几个对象？各自只负责一件什么事？

## A
`RateLimiter`：按 key 找到状态、加锁、调用算法。`Algorithm`（每个 key 一份状态）：只回答 `allow(now)`。`Decision`（allowed、remaining、retry_after）：一次判定的结果。时钟 `clock` 从构造函数注入。切分依据：「怎么记住最近的流量」会换（固定窗口、令牌桶……），「按 key 隔离并加锁」不变。
