---
id: traffic-http2-connection-pinning
node: traffic.load-balancing
type: qa
---
## Q
You put gRPC services behind an L4 load balancer; one backend runs hot while new instances sit idle. Why, and what are the fixes?

## A
L4 balances **connections**, and gRPC/HTTP-2 clients open one long-lived multiplexed connection — every request from a client pins to whichever backend won the initial pick. Scale-outs get nothing: existing connections never move.

- **L7 proxy** (Envoy/ALB) balancing per-request/per-stream instead of per-connection.
- **Client-side load balancing**: client resolves the backend set and picks per request (often over a subset).
- Blunt backstop: server-enforced `max-connection-age` forcing periodic reconnect and re-pick.

## Q zh
你把 gRPC 服务放在 L4 负载均衡器后面；一个后端运行热，新实例空闲。为什么，修复是什么？

## A zh
L4 平衡**连接**，gRPC/HTTP-2 客户端打开一个长期多路复用连接 — 来自客户端的每个请求固定在赢得初始选择的后端 — 扩展没有收获：现有连接永远不会移动。

- **L7 代理**（Envoy/ALB）平衡每请求/每流而不是每连接。
- **客户端负载平衡**：客户端解析后端集并按请求选择（通常在子集上）。
- 钝后挡板：服务器强制 `max-connection-age` 强制定期重新连接并重新选择。
