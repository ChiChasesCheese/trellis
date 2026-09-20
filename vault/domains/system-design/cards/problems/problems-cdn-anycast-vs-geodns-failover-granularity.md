---
id: problems-cdn-anycast-vs-geodns-failover-granularity
node: problems.foundations.cdn
type: qa
step: 2
tags: [grown]
---
## Q
When designing the request-routing layer of a CDN, why does choosing anycast (the same IP announced from every PoP via BGP) over GeoDNS (a resolver returning different IPs per region) fundamentally change how fast the system can fail over a dead PoP, rather than just how it's implemented?

## A
With GeoDNS, failover means the authoritative DNS server changes which IP it returns, but clients and resolvers keep using a cached answer until its TTL expires - and some resolvers or apps ignore TTLs entirely - so a dead PoP keeps receiving traffic for minutes. With anycast, failover is a network-layer event: the dead PoP withdraws its BGP route announcement, and internet routers recompute the shortest AS-path to the next PoP announcing that same IP - no DNS cache, no client behavior, and no TTL is involved, so convergence happens in seconds. The trade-off is that anycast gives up GeoDNS's fine-grained, centrally controlled routing (e.g., steering by customer tier or capacity) in exchange for that faster, DNS-independent failover.

## Q zh
在设计 CDN 的请求路由层时，为什么选择 anycast（所有 PoP 通过 BGP 宣告同一个 IP）而不是 GeoDNS（解析器根据区域返回不同 IP），会从根本上改变系统对一个死亡 PoP 的故障转移速度，而不仅仅是实现方式的不同？

## A zh
用 GeoDNS 时，故障转移意味着权威 DNS 服务器改变它返回的 IP，但客户端和解析器会继续使用已缓存的答案直到 TTL 过期——而且有些解析器或应用完全忽略 TTL——所以死亡 PoP 会继续收到流量好几分钟。用 anycast 时，故障转移是一个网络层事件：死亡 PoP 撤回它的 BGP 路由宣告，互联网路由器重新计算到同一 IP 的下一个最短 AS-path——不涉及 DNS 缓存、客户端行为或任何 TTL，收敛发生在秒级。代价是 anycast 放弃了 GeoDNS 的细粒度、集中控制的路由能力（如按客户等级或容量进行调度），换取这种更快、不依赖 DNS 的故障转移。
