---
id: kafka-admin-client-dns-lookup-modes
node: admin.topic-ops
type: qa
source: kafka-2e
---
## Q
客户端连接配置参数 `client.dns.lookup` 有 `resolve_canonical_bootstrap_servers_only` 和 `use_all_dns_ips` 两个可选值，分别是为了解决什么部署场景下的连接问题？

## A
场景一：用一个 DNS 别名（如 `all-brokers.hostname.com`）统一代表多个 broker 的真实主机名，并启用了 SASL 身份验证——客户端会拿别名去做服务器身份验证，但实际连上的 broker 主体却是它自己的主机名，名字不匹配会被 SASL 拒绝；这时配置 `resolve_canonical_bootstrap_servers_only`，让客户端把别名「展开」成真实的 broker 主机名列表再逐个验证。场景二：一个域名背后是负载均衡器映射出的多个 IP（常见于 Kubernetes 环境）——默认客户端只连接第一个解析到的 IP，如果这个 IP 恰好不可用就直接连接失败，即使 broker 本身正常；这时配置 `use_all_dns_ips`，让客户端在解析出的多个 IP 之间尝试，从而真正用上负载均衡带来的高可用性。
