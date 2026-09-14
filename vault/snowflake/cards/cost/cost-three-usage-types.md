---
id: cost-three-usage-types
node: cost.credit-model-per-second-billing
type: qa
source: snowflake-docs
---
## Q
一份 Snowflake 账单由哪三类用量构成？每一类分别怎样计价？

## A
(1) 计算（compute）：消耗信用点（credit），账单金额 = 消耗的信用点数 × 信用点单价；计算又分虚拟仓库、无服务器（serverless）功能和云服务三类。(2) 存储（storage）：按每 TB 固定月费率计价，按每天账户中平均落盘字节数（压缩后）计算。(3) 数据传输（data transfer）：导入数据不收入站费，但把数据传出到同云的其他区域或另一个云平台时，按每 TB 收取出站（egress）费用。存算分离的架构使得每项任务的成本都能归入这三类之一。
