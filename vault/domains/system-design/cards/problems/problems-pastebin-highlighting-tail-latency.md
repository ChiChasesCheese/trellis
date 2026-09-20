---
id: problems-pastebin-highlighting-tail-latency
node: problems.foundations.pastebin
type: qa
step: 7
tags: [grown]
---
## Q
In a pastebin design, synchronous server-side syntax highlighting only needs an estimated ~2 CPU cores fleet-wide to keep up with peak read traffic, yet the design still defaults to client-side highlighting. Why, if the aggregate cost is so small?

## A
Because the aggregate CPU cost hides a tail-latency problem: highlighting a large paste (e.g. a multi-megabyte log dump) synchronously on the server can take over a second at typical lexer throughput, which blows through a sub-second read-latency budget for that single request — and large pastes are not a rare edge case, since a small fraction of pastes by count routinely accounts for the large majority of bytes served. Defaulting to client-side rendering moves that cost onto the requester's own browser and keeps the server's response time independent of paste size; only small pastes below a size threshold get a one-time server-side pre-render at write time, since their per-request cost is low and rendering once amortizes across all future reads of that paste.

## Q zh
在一个 pastebin 设计中，服务端同步语法高亮据估算全机群只需要约 2 个 CPU 核心就能撑住峰值读流量，但设计仍然默认走客户端高亮。既然聚合成本这么小，为什么还要这样选？

## A zh
因为聚合 CPU 成本掩盖了一个尾延迟问题：在典型的词法高亮器吞吐下，同步为一条大粘贴（例如几兆字节的日志转储）做服务端高亮可能耗时超过一秒，直接击穿这一次请求本应是亚秒级的读延迟预算——而大粘贴并不是罕见的边缘情况，因为很小一部分（按条数）粘贴通常贡献了被服务的绝大多数字节量。默认走客户端渲染把这份成本转移到请求方自己的浏览器上，让服务端响应时间与粘贴大小无关；只有小于某个尺寸阈值的粘贴才会在写入时做一次性的服务端预渲染，因为它们单次渲染成本低，而且渲染一次就能被这条粘贴之后所有读取复用。
