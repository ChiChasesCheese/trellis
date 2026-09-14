---
id: netpol-allowlist-implicit-block
node: security.network-policies-private-connectivity
type: qa
source: snowflake-docs
---
## Q
给 Snowflake 的网络策略（network policy，按请求来源允许或拒绝入站访问的策略）的允许列表（allowed list）加入一条只含一个 IPv4 地址的网络规则后，其他 IPv4 地址还需要再放进阻止列表（blocked list）吗？同一个地址同时出现在两个列表里又会怎样？

## A
不需要。允许列表一旦包含某类标识符，同类型的其他所有标识符就被隐式阻止，只有列入允许的来源可访问。若同一 IP 同时出现在允许和阻止列表中，Snowflake 先应用阻止列表，即该地址被拒绝。阻止列表的典型用途是“允许一个网段但排除其中某个地址”：允许列表放 `192.168.1.0/24`，阻止列表放 `192.168.1.99`。
