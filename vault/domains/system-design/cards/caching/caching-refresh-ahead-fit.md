---
id: caching-refresh-ahead-fit
node: caching.strategies
type: qa
---
## Q
When is refresh-ahead worth the complexity over plain TTL + cache-aside, and what does it waste when misapplied?

## A
Refresh-ahead asynchronously reloads a key *before* its TTL expires, so hot keys never pay a miss.

- Worth it when: a small, predictable set of hot keys, expensive recomputation, and strict tail-latency SLOs (a miss = user-visible spike).
- Misapplied on a long-tail keyspace it **refreshes keys nobody will read again**, multiplying backend load instead of reducing it.

Rule of thumb: refresh-ahead for the head of the distribution, TTL-on-demand for the tail.

## Q zh
什么时候 refresh-ahead 值得在普通 TTL + cache-aside 上的复杂性，当误用时它浪费什么？

## A zh
Refresh-ahead 在 TTL 过期 *之前* 异步重新加载键，所以热键永远不支付 miss。

- 值得当：一个小的、可预测的热键集合、昂贵的重新计算和严格的尾延迟 SLO（miss = 用户可见的尖峰）。
- 误用在长尾键空间上 **刷新没有人会再读的键**，乘以后端负载而不是减少它。

经验法则：refresh-ahead 用于分布的头部，按需 TTL 用于尾部。
