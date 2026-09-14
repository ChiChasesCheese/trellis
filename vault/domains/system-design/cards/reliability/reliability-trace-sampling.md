---
id: reliability-trace-sampling
node: reliability.observability
type: qa
---
## Q
Head-based vs tail-based trace sampling — what does each decide on, and which one keeps the traces you actually want during an incident?

## A
- **Head-based**: sample decision made at the first hop (e.g. keep 1%), propagated via the trace context so all spans of a kept trace survive. Cheap and simple — but errors and slow requests are rare, so the interesting 1-in-10k trace is usually dropped.
- **Tail-based**: buffer all spans, decide after the trace completes — keep every error and p99-slow trace, sample the boring ones. Exactly what incidents need, at the cost of a buffering/collection tier that must see the whole trace.

## Q zh
头部采样 vs 尾部采样追踪——每个决定什么，哪个在事故期间保持你实际想要的追踪？

## A zh
- **头部采样**：采样决定在第一跳做（例如保持 1%），通过追踪上下文传播所以保持的追踪的所有跨度都生存。便宜和简单——但错误和慢请求很少，所以有趣的 1 在 10k 追踪通常被丢弃。
- **尾部采样**：缓冲所有跨度，在追踪完成后决定——保持每个错误和 p99 慢追踪，采样无聊的。正好是事故需要，代价是必须看到整个追踪的缓冲/收集层。
