---
id: networking-cdn-stale-while-revalidate
node: networking.cdn
type: qa
---
## Q
`Cache-Control: stale-while-revalidate` and `stale-if-error` — what does each authorize a CDN to do, and what do you buy?

## A
- **stale-while-revalidate=N**: for N seconds after TTL expiry, serve the stale copy *immediately* while refetching in the background — popular keys never make a user pay origin latency, and staleness stays bounded by the window.
- **stale-if-error=N**: if the origin errors or is unreachable, keep serving the expired copy for up to N — availability from cache through an origin outage.

Both trade strict freshness for latency and availability — the right default for content where seconds-old is indistinguishable from fresh.

## Q zh
`Cache-Control: stale-while-revalidate` 和 `stale-if-error` — 每个授权 CDN 做什么，你获得什么好处？

## A zh
- **stale-while-revalidate=N**：TTL 过期后的 N 秒内，立即提供过时副本*同时*在后台重新获取 — 热门 key 永远不会让用户支付源站延迟，陈旧性保持在窗口内有界。
- **stale-if-error=N**：如果源站出错或不可达，继续提供过期副本长达 N 秒 — 通过源站故障的缓存提供可用性。

两者都用严格的新鲜度换取延迟和可用性 — 对于几秒旧的内容与新内容无法区分的场景来说是正确的默认行为。
