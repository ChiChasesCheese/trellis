---
id: networking-cdn-dynamic-acceleration
node: networking.cdn
type: qa
---
## Q
Your API responses are fully personalized and uncacheable. What does routing them through a CDN still buy?

## A
- **Handshakes on a short path**: TCP/QUIC + TLS terminate at an edge ~10–20 ms away instead of 150 ms cross-continent — saving 1–2 RTTs where RTTs are cheap.
- **Warm pooled edge→origin connections**: no per-client handshake ever reaches the origin.
- **Private backbone routing**: edge-to-origin rides the provider's network, typically beating public-internet transit paths.
- **Edge absorption of hostile traffic**: WAF, bot filtering, DDoS soak before your infra.

Net effect: meaningfully lower cross-continent API latency with zero caching involved.

## Q zh
API 响应完全个性化且不可缓存。通过 CDN 路由它们仍然能带来什么好处？

## A zh
- **短路径上的握手**：TCP/QUIC + TLS 在距离约 10-20 ms 的边缘终止，而不是跨洲际的 150 ms — 节省 1-2 个 RTT（RTT 很廉价）。
- **预热的连接池边缘→源站连接**：没有单个客户端的握手会到达源站。
- **私有骨干网路由**：边缘到源站使用提供商的网络，通常比公网传输路径更优。
- **边缘吸收敌意流量**：WAF、bot 过滤、DDoS 吸收都在基础设施之前进行。

净效果：跨洲际 API 延迟显著降低，完全不涉及缓存。
