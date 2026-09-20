---
id: problems-url-shortener-kgs-outage
node: problems.foundations.url-shortener
type: qa
step: 7
tags: [grown]
---
## Q
In a URL shortener design, if the key-generation coordination service (KGS) that hands out short-code ranges becomes unavailable, what happens to link creation versus link redirection, and why?

## A
Link creation degrades or fails — writer instances that have exhausted their locally cached batch of codes can't obtain a new range and start rejecting create requests — but link redirection is completely unaffected, because the redirect path depends only on the cache and the primary key-value store, never on the KGS. This isolation is a direct consequence of decoupling the low-QPS write path (which needs the KGS) from the high-QPS read path (which doesn't); a KGS outage of a few minutes is tolerable because writer instances pre-fetch batches (e.g., 1,000 codes) and don't call the coordinator on every request.

## Q zh
在一个短链接设计中，如果负责分配短码区间的短码生成协调服务（KGS）不可用了，链接创建和链接重定向分别会受到什么影响，为什么？

## A zh
链接创建会降级或失败——本地缓存的短码批次已耗尽的写服务实例无法获取新区间，开始拒绝创建请求——但链接重定向完全不受影响，因为重定向路径只依赖缓存和主键值存储，从不依赖 KGS。这种隔离性质是把低 QPS 的写路径（依赖 KGS）和高 QPS 的读路径（不依赖 KGS）解耦的直接结果；由于写服务实例会预取批次（例如每批 1,000 个短码），并不需要每次请求都联系协调服务，几分钟的 KGS 中断是可以容忍的。
