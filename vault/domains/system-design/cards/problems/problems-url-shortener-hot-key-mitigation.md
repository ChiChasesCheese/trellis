---
id: problems-url-shortener-hot-key-mitigation
node: problems.foundations.url-shortener
type: qa
step: 4
tags: [grown]
---
## Q
In a URL shortener design, a single viral short link can push traffic on one cache shard far above the system's overall peak (thousands of QPS on one key while the system-wide peak is only around 5,800 QPS). What two mechanisms address this hot-key problem specifically, as opposed to just adding more cache capacity?

## A
(1) Request coalescing / single-flight: when a hot key's cache entry expires, concurrent cache misses for that key are merged so only one request goes to the database while the rest wait on that single result, preventing a cache-stampede (thundering herd) from overwhelming the database. (2) Hot-key replication: once a key's access rate crosses a threshold, its value is replicated across multiple cache nodes and clients are routed to one of the replicas, trading memory for the ability to serve one key at a rate no single cache node could sustain alone.

## Q zh
在一个短链接设计中，一条爆款（viral）短链可能把单个缓存分片的流量推到远高于系统整体峰值的水平（单键达到数千 QPS，而系统整体峰值只有约 5,800 QPS）。有哪两种机制专门用来解决这种热点键（hot key）问题，而不是单纯增加缓存容量？

## A zh
（1）请求合并 / single-flight：当热点键的缓存条目过期时，把针对该键的并发缓存未命中请求合并，只让一个请求打到数据库，其余请求等待这一个结果，从而防止缓存失效风暴（thundering herd）打垮数据库。（2）热点键复制：一旦某个键的访问频率超过阈值，就把它的值复制到多个缓存节点上，客户端路由到其中一个副本，用空间换取单个键的水平扩展能力，而不是依赖单个缓存节点独自扛住。
