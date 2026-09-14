---
id: netpol-network-rules-vs-ip-list
node: security.network-policies-private-connectivity
type: qa
source: snowflake-docs
---
## Q
新建网络策略时，为什么推荐用网络规则（network rule）而不是旧的 `ALLOWED_IP_LIST` / `BLOCKED_IP_LIST` 参数？网络规则本身决定“允许”还是“阻止”吗？

## A
网络规则是模式级对象，把同一类型（如 IPv4、VPCE ID）的相关标识符打包成小而有注释的逻辑单元（如“北美客户端 IP”“高权限服务账号来源”），便于复用、审计和按人群精细挂载，取代以往巨大的单体 IP 列表。规则本身不表示允许或阻止，它只是分组；由网络策略把它放进允许列表或阻止列表来决定语义。最佳实践是同一策略中不要混用新旧两种方式。
