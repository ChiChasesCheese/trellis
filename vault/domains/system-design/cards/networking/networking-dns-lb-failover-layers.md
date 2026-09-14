---
id: networking-dns-lb-failover-layers
node: networking.dns
type: qa
---
## Q
Health-checked DNS (e.g. Route 53) can drop a dead region from its answers. Why do you still need LB-level failover underneath — how is the labor divided?

## A
DNS failover operates at **minutes** granularity: health-check interval + record TTL + resolvers that ignore TTLs ([[networking-dns-ttl-failover]]). That's acceptable — and the only option — at *region/site* level, where the failing targets have different IPs.

*Instance* failure needs **seconds**: the load balancer's health checks eject a dead backend before the next request, behind the same VIP, with clients never involved.

Layered rule: GSLB/DNS chooses the region; the LB chooses the instance. Using DNS for instance failover means minutes of errors per dead host.

## Q zh
健康检查的 DNS（例如 Route 53）可以从答案中删除死亡地域。为什么你仍然需要 LB 级故障转移在下面 — 工作如何分配？

## A zh
DNS 故障转移在**分钟**粒度运作：健康检查间隔 + 记录 TTL + 忽略 TTL 的解析器（[[networking-dns-ttl-failover]]）。这是可以接受的 — 也是唯一选择 — 在*地域/站点*级，失败的目标有不同的 IP。

*实例*故障需要**秒级**：负载均衡器的健康检查在下一个请求前清除死后端，在同一 VIP 后面，客户端从不参与。

分层规则：GSLB/DNS 选择地域；LB 选择实例。使用 DNS 进行实例故障转移意味着每个死主机每分钟的错误。
