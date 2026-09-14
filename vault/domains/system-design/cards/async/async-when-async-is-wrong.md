---
id: async-when-async-is-wrong
node: async.queues
type: qa
---
## Q
Name three signals that making an operation asynchronous (via a queue) is the wrong call.

## A
- The caller **needs the result to proceed** (auth check, price quote, inventory reservation shown to the user) — you'd just rebuild synchronous RPC with extra latency and a callback.
- The operation must **fail visibly to the user** so they can correct input; a queued failure surfaces minutes later with no one watching.
- The workload is **low-volume and latency-sensitive** — the queue adds hops, ops burden, and delivery-semantics complexity with no smoothing benefit.

Async pays off for: bursty load, slow side effects, retryable work, fan-out.

## Q zh
列出三个信号，表示通过队列使操作异步是错误的选择。

## A zh
- 调用者**需要结果来继续**（auth 检查、价格报价、库存保留显示给用户）— 你只是用额外延迟和回调重建同步 RPC。
- 操作必须**对用户可见地失败**，使他们能更正输入；排队的失败分钟后浮现，没人观看。
- 工作负载是**低量和延迟敏感的** — 队列添加跳跃、ops 负担、投递语义复杂性，没有平滑好处。

Async 付费对象：突发负载、缓慢副作用、可重试工作、扇出。
