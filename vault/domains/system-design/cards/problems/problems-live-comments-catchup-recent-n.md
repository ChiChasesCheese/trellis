---
id: problems-live-comments-catchup-recent-n
node: problems.social.live-comments
type: qa
step: 6
tags: [grown]
---
## Q
A viewer joins a live video 20 minutes after it started, during which roughly 200,000 comments have accumulated at peak rate. What catch-up strategy should the system use for this late-joining viewer, and why not replay the full backlog?

## A
The system serves a fixed-size recent window — e.g. the last 50 comments via a `GET /videos/{id}/comments/recent?limit=50` call — as initial context, then switches the viewer to the live broadcast stream going forward. Replaying all 200,000 accumulated comments has no product value (no viewer reads that much) and forces an unnecessarily large query against the comment store at the exact moment a viewer joins — a query whose cost would only grow the longer the stream has been running. The same fixed-window mechanism is reused for reconnection after a brief disconnect, rather than maintaining a precise per-viewer "last seen" watermark for every one of potentially millions of viewers, which would be a large new storage and consistency problem for a benefit (never missing a single comment) the product doesn't actually require.

## Q zh
一个观众在直播开始 20 分钟后才加入，此时按峰值速率已经累积了约 20 万条评论。系统应该给这位迟到观众用什么追赶策略？为什么不重放全部历史？

## A zh
系统提供一个固定大小的最近窗口作为初始上下文——例如通过 `GET /videos/{id}/comments/recent?limit=50` 拿最近 50 条——然后把该观众切换到向前的实时广播流。重放累积的全部 20 万条评论没有产品价值（没有观众会读这么多），还会在观众加入的瞬间对评论存储发起一次不必要的大查询——而且这个查询代价会随直播进行时间越长而越大。同样的固定窗口机制也用于短暂断线后的重连，而不是为潜在数百万观众中的每一个都维护精确的"已读到哪条"水位线，那会是一个规模很大的新存储和一致性问题，换来的收益（一条评论都不错过）产品上并不需要。
