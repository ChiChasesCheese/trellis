---
id: caching-cache-warming
node: caching.strategies
type: qa
---
## Q
A new cache cluster (or one recovering from a flush) goes live cold. What happens at cutover, and what are three warming techniques?

## A
Hit rate starts at ~0%, so the database briefly receives the *full* read load it was never provisioned for — the cold-start herd can take it down (the math: [[caching-hit-rate-outage-math]]).

- **Shadow reads**: mirror production read traffic to the new tier for a while before cutover so it fills organically.
- **Preload**: replay a key-popularity log or copy hot entries from the old cluster/a snapshot.
- **Gradual ramp**: shift traffic in percentage steps sized so miss traffic stays inside DB headroom.

Same discipline applies after any mass-expiry event ([[caching-ttl-jitter]]).

## Q zh
一个新的缓存集群（或从刷新中恢复的）冷启动。在切换时会发生什么，有三种预热技术是什么？

## A zh
命中率从 ~0% 开始，所以数据库短暂地接收它从未为之配置的 *完整* 读负载 — 冷启动羊群可能会将其击落（数学：[[caching-hit-rate-outage-math]]）。

- **影子读**：在切换前一段时间将生产读流量镜像到新层，使其有机地填充。
- **预加载**：重放键热门日志或从旧集群/快照复制热条目。
- **逐步斜升**：以百分比步骤转移流量，大小使得 miss 流量保持在 DB 余量内。

相同的纪律适用于任何质量过期事件之后（[[caching-ttl-jitter]]）。
