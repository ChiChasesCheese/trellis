---
id: problems-distributed-cache-fanout-multiplier-qps
node: problems.foundations.distributed-cache
type: qa
step: 1
tags: [grown]
---
## Q
In a distributed cache design, why does the fan-out multiplier (distinct cache keys fetched per user page load) matter more for sizing cache QPS than the raw user action rate does, and how does this differ from sizing a durable key-value store?

## A
A durable key-value store's QPS tracks the rate of user-triggered operations directly. A look-aside cache's QPS instead tracks that rate multiplied by however many independent cache lookups one page load triggers, because a page is assembled from many components that each query their own cache entries. In one estimate at 200M DAU with 15 requests/day and 40 keys fetched per request, peak cache QPS reaches ≈4,166,667 — a number driven almost entirely by the fan-out multiplier, not by how often users act. Facebook has publicly disclosed an average of 521 distinct memcache items fetched per popular page load, an order of magnitude higher, underscoring that this multiplier must be measured per application, not assumed.

## Q zh
在分布式缓存设计中，为什么「每次页面加载触发多少个不同缓存 key 查询」这个放大倍数，比原始用户操作速率更能决定缓存 QPS？这和为一个可持久化键值存储做容量估算有什么不同？

## A zh
可持久化键值存储的 QPS 直接跟踪用户触发操作的速率。旁路缓存的 QPS 则要再乘以「一次页面加载触发多少次独立缓存查询」这个倍数，因为页面是由多个各自查询自己缓存条目的组件拼装而成的。在一个 2 亿日活、每天 15 次请求、每次请求 40 个 key 的估算里，峰值缓存 QPS 达到约 4,166,667——这个数字几乎完全由放大倍数决定，而不是由用户实际操作频率决定。Facebook 曾公开披露热门页面平均每次加载触发约 521 次不同的 memcache 条目查询，比这个例子高一个数量级，说明这个倍数必须针对具体应用实际测量，不能凭空假设。
