---
id: hi-sd-networking-essentials-5-lb-types
node: qb.sd.messenger-chat-system.pre-sd-core-concepts-networking-essentials
type: qa
step: 5
---
## Q
**客户端与专用负载均衡**｜系统设计 · 核心概念

水平扩展后要决定请求发给哪台服务器。客户端负载均衡与专用负载均衡有什么区别？专用的 L4 与 L7 又怎样选？

## A
**要点。**
- 客户端负载均衡：客户端从服务注册表拿到服务器列表，自己选一台直连，省掉一跳；例子有 Redis Cluster（客户端对 key 哈希找分片，打错节点会收到 MOVED）、gRPC、DNS 轮转（受 TTL 限制，更新慢）。适合客户端少且可控，或能容忍更新慢。
- 专用负载均衡：多一跳，但服务器列表更新快、路由控制细。
- **2026 亮点：** 多可用区部署还要管跨 AZ 流量：K8s 的 Service 设 trafficDistribution: PreferSameZone（1.35 起稳定），数据面优先把请求发给同 AZ 的端点，同 AZ 没有健康端点才回退到别的 AZ，既降延迟又省跨 AZ 流量费。代价是各 AZ 的副本数和流量要大致均衡，否则少数端点被打热，要配合 topology spread 把副本按 AZ 均匀打散。

**取舍。** L4 只看 IP 和端口，转发 TCP 连接，快、不解析内容，同一连接始终落在同一台，适合 WebSocket。L7 终止连接再转发请求，能按 URL、头部、Cookie 路由，更耗 CPU，适合 HTTP 与长轮询，也能当简易 API 网关。

**易错。** 负载均衡器本身是单点：用 DNS 轮转多个均衡器，并放在不同机房或区域。面试中用 WebSocket 就选 L4，其余默认 L7。
