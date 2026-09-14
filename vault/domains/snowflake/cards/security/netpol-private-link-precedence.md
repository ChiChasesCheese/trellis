---
id: netpol-private-link-precedence
node: security.network-policies-private-connectivity
type: qa
source: snowflake-docs
---
## Q
网络策略的允许列表里有一条 `AWSVPCEID`（AWS PrivateLink 的 VPC 端点 ID）类型的网络规则，还有若干 IPv4 规则。一个经私有连接进来的请求会怎么被判定？这条 VPCE 规则能挡住公网流量吗？

## A
私有连接类规则（`AWSVPCEID`、`AZURELINKID`）优先于 IPv4/IPv6 规则：私有连接请求若命中允许列表中的这类规则，所有 IPv4/IPv6 规则都被忽略。但基于私有端点标识符的规则对公网请求没有任何作用，所以若要“只允许某个 VPCE、同时完全拒绝公网”，必须建两条规则：VPCE 规则放允许列表，另一条覆盖公网 IPv4 的规则（如 `0.0.0.0/0`）放阻止列表。
