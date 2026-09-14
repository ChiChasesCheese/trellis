---
id: traffic-l4-vs-l7
node: traffic.load-balancing
type: qa
---
## Q
L4 vs L7 load balancer — what does each see, and when is L4 the right choice despite L7's flexibility?

## A
- **L4** sees only IP+port: forwards TCP/UDP flows, no payload inspection. Extremely fast, millions of connections, protocol-agnostic.
- **L7** terminates the connection and sees the request: path/header routing, TLS termination, retries, per-route policies.

Choose **L4** for raw throughput or non-HTTP traffic (databases, MQTT, game servers, WebSocket passthrough at huge scale) — or as the resilient tier **in front of** the L7 fleet, which is the common stacked pattern.

## Q zh
L4 vs L7 负载均衡器 — 每个看到什么，什么时候 L4 是正确的选择尽管 L7 的灵活性？

## A zh
- **L4** 仅看到 IP+port：转发 TCP/UDP 流，没有有效载荷检查。极其快速、数百万连接、协议无关。
- **L7** 终止连接并看到请求：路径/头路由、TLS 终止、重试、每个路由策略。

选择**L4**用于原始吞吐或非 HTTP 流量（数据库、MQTT、游戏服务器、WebSocket 大规模直通）— 或作为L7 舰队*前面*的弹性层，这是常见的堆叠模式。
