---
id: networking-dns-negative-caching
node: networking.dns
type: qa
---
## Q
You delete a DNS record by mistake and resolvers start returning NXDOMAIN. You fix the zone — but clients keep failing. Why?

## A
**Negative caching**: resolvers cache NXDOMAIN/NODATA answers too, for the negative TTL — min(SOA MINIMUM field, SOA record's own TTL). Your fix only takes effect as those cached denials expire, so a misconfiguration outage outlives its correction.

Ops takeaways: keep the negative TTL modest (minutes, not hours), and remember the mechanism exists *for* a reason — it shields authoritative servers from repeated lookups of nonexistent names (typo storms, misconfigured clients).

## Q zh
你错误地删除了 DNS 记录，解析器开始返回 NXDOMAIN。你修复了区域 — 但客户端继续失败。为什么？

## A zh
**负向缓存**：解析器也缓存 NXDOMAIN/NODATA 答案，使用负向 TTL — min(SOA MINIMUM 字段, SOA 记录自己的 TTL)。你的修复只有在这些缓存的拒绝过期后才生效，所以一个配置错误的中断会比其修复更久。

运维要点：保持负向 TTL 适度（分钟，而不是小时），并记住这个机制存在*是有*原因的 — 它保护权威服务器免于重复查找不存在的名称（打字风暴、配置错误的客户端）。
