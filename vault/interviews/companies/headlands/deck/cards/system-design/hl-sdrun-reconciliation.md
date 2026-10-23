---
id: hl-sdrun-reconciliation
node: system-design.how-to-run
type: qa
step: 31
---
## Q
对账（reconciliation）分哪几层？发现差异（break）后先做什么？

## A
- **实时**：独立的 **drop copy** 会话，交易所把我们所有成交副本发到另一条通道，与内部订单状态机比对；
- **日终**：与清算 / 经纪商的头寸和成交对账。

发现差异（break）→ **先停**该品种或该策略（fail closed），再查原因。
