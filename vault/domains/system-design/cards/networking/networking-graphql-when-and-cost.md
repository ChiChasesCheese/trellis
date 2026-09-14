---
id: networking-graphql-when-and-cost
node: networking.api-styles
type: qa
---
## Q
What client situation makes GraphQL earn its complexity, and what two operational problems does it import?

## A
Earns it when **many diverse clients need different slices of the same graph** (mobile vs web vs partners) — clients query exactly the fields they need, killing over-/under-fetching and per-client backend endpoints (BFFs).

Costs:
- **Caching gets hard**: everything is a POST to one endpoint, so HTTP/CDN caching no longer works for free.
- **Unbounded query cost**: clients can write pathological nested queries — you must add depth/complexity limits and solve N+1 with dataloaders.

## Q zh
什么客户端情况使 GraphQL 值得其复杂性，它带入什么两个运维问题？

## A zh
当**许多不同的客户端需要同一图的不同切片**（mobile vs web vs 合作伙伴）时值得 — 客户端只查询它们需要的字段，消除过度/不足获取和每客户端后端端点（BFF）。

代价：
- **缓存变得困难**：一切都是对一个端点的 POST，所以 HTTP/CDN 缓存不再免费工作。
- **无界查询成本**：客户端可以编写病态嵌套查询 — 你必须添加深度/复杂性限制并用 dataloader 解决 N+1。
