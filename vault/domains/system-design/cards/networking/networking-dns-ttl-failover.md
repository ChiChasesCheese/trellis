---
id: networking-dns-ttl-failover
node: networking.dns
type: qa
---
## Q
Why is DNS a blunt instrument for failover, and what two things do teams do about it?

## A
Because you can't force clients to forget: cached records live until **TTL expires**, and some resolvers/apps ignore TTLs or pin connections — so after a DNS switch, traffic bleeds to the dead endpoint for minutes.

- **Pre-drop TTL** (e.g. 60 s) on records you may need to move — accepting more resolver load.
- **Fail over below DNS instead**: anycast IPs or a load balancer VIP, so the IP stays the same and rerouting is instant.

## Q zh
为什么 DNS 是故障转移的钝工具，团队对此做什么两件事？

## A zh
因为你无法强制客户端忘记：缓存的记录持续到 **TTL 过期**，一些解析器/应用忽略 TTL 或固定连接 — 所以在 DNS 切换后，流量流向死端点数分钟。

- **预先降低 TTL**（例如 60 s）用于你可能需要移动的记录 — 接受更多解析器负载。
- **在 DNS 下故障转移**：anycast IP 或负载均衡器 VIP，所以 IP 保持不变且重路由是即时的。
