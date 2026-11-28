---
id: hi-c-sd-dynamodb-n09-consistency
node: sd.deep-dives.dynamodb.notes
type: qa
step: 7
---
## Q
**DynamoDB · 一致性：按每次读取选择**｜摘要 · 必会

DynamoDB 是 AP 还是 CP？一致性是怎么配置的？事务支持到什么程度？

## A
- **按请求选择：** 不是表级配置；每次 GetItem、Query、Scan 设置 `ConsistentRead=true` 即强一致，默认是最终一致。
- **最终一致（默认）：** 可用性最高、延迟最低，可能暂时读不到最新写入；整体表现像带 BASE 特性的 AP 系统。
- **强一致：** 读到的结果包含此前所有成功的写入，读容量翻倍（每 4 KB 消耗 1 个 RCU，最终一致只要 0.5 个），延迟略高。
- **灵活之处：** 订座等少数路径用强一致，读多且对延迟敏感的路径用默认。
- **限制：** 强一致读只支持主表和 LSI，GSI 只能最终一致。
- **事务：** `TransactWriteItems` 和 `TransactGetItems` 提供 ACID，可覆盖最多 100 个项、跨多张表，隔离级别为可串行化。
