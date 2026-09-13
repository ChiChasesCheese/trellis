---
id: reliability-tracing-cache-hit-span
node: reliability.tracing
type: qa
---
## Q
Should an edge cache HIT create a trace even though it makes no origin call? What should that trace show?

## A
Yes, for the sampled request. Create a server span for the edge decision with cache tier/outcome, representation key class, response size, and region; do not invent an origin span. This lets HIT latency and routing be compared with MISS traces and prevents tracing from representing only slow dependency paths.

## Q zh
edge cache HIT 没有 origin call，还应该创建 trace 吗？这个 trace 应展示什么？

## A zh
对于被 sample 的 request，应该创建。为 edge decision 创建 server span，记录 cache tier/outcome、representation key class、response size 和 region；不要虚构 origin span。这样可以比较 HIT latency 与 MISS trace，也避免 tracing 只代表缓慢的 dependency path。
