---
id: reliability-rpo-vs-rto
node: reliability.multi-region
type: qa
---
## Q
RPO vs RTO: which one is about data, which about time-to-recover, and which replication choice controls each?

## A
- **RPO (Recovery Point Objective)**: max acceptable **data loss**, measured backward from the failure. Controlled by replication mode — synchronous replication gives RPO ≈ 0; async gives RPO = replication lag; nightly backups give RPO up to 24h.
- **RTO (Recovery Time Objective)**: max acceptable **downtime** until service is restored. Controlled by failover automation and standby warmth (active-active ≈ seconds; cold restore ≈ hours).

They are independent knobs: you can have RPO 0 with a slow manual failover (RTO hours), or instant failover that drops recent writes.

## Q zh
RPO vs RTO：哪个关于数据，哪个关于恢复时间，哪个复制选择控制每个？

## A zh
- **RPO（恢复点目标）**：最大可接受**数据丢失**，从失败向后测量。由复制模式控制——同步复制给 RPO ≈ 0；异步给 RPO = 复制延迟；每夜备份给 RPO 直到 24h。
- **RTO（恢复时间目标）**：最大可接受**停机时间**直到服务恢复。由故障转移自动化和备用热度控制（active-active ≈ 秒；冷恢复 ≈ 小时）。

它们是独立旋钮：你可以有 RPO 0 与慢手动故障转移（RTO 小时），或即时故障转移丢弃最近写。
