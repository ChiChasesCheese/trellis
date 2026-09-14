---
id: networking-anycast-vs-geodns
node: networking.dns
type: qa
---
## Q
Anycast vs GeoDNS for steering users to the nearest site — mechanism and weakness of each?

## A
- **Anycast**: the *same* IP announced via BGP from many sites; the network routes each client to the topologically closest. Failover is instant (withdraw the route) and DNS-invisible — but you don't control the mapping (BGP does), and a route flap can shift mid-connection, so it favors short flows and UDP (DNS roots, CDN edges).
- **GeoDNS/GSLB**: the authoritative server returns *different* IPs based on where the query comes from. Fine-grained control and weighted splits — but it sees the **resolver's** location, not the client's (public resolvers mislocate; EDNS Client Subnet only partially fixes it), and every change is TTL-bound.

Big CDNs use both: GeoDNS to pick a region, anycast within it.

## Q zh
Anycast 和 GeoDNS 用于将用户导向最近的站点 — 各自的机制和弱点是什么？

## A zh
- **Anycast**：从多个站点通过 BGP 宣告*相同*的 IP；网络将每个客户端路由到拓扑最近的站点。故障转移是即时的（撤回路由），对 DNS 透明 — 但你无法控制映射关系（BGP 控制），路由抖动可能在连接中途改变路由，因此它适合短连接和 UDP（DNS 根、CDN 边缘）。
- **GeoDNS/GSLB**：权威服务器根据查询来源返回*不同*的 IP。细粒度控制和加权分流 — 但它看到的是**解析器**的位置，而不是客户端的位置（公共解析器定位不准；EDNS Client Subnet 只能部分解决），每次变更都受 TTL 限制。

大型 CDN 同时使用两者：GeoDNS 选择地区，anycast 在地区内部。
