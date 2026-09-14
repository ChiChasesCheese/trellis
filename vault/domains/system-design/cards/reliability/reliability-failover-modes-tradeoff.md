---
id: reliability-failover-modes-tradeoff
node: reliability.availability
type: qa
---
## Q
Rank hot, warm, and cold standby failover by recovery speed, and name the hidden risk hot standby adds.

## A
- **Hot (active-active or synced active-passive)**: seconds — standby already serves or has current state. Costs ~2x and risks **split-brain**: both nodes believe they are primary, so you need fencing/quorum before promoting.
- **Warm**: minutes — replica running but lagging; failover loses the replication-lag window of writes.
- **Cold**: hours — restore from backup; data loss up to last backup.

## Q zh
按恢复速度对 hot、warm 和 cold standby failover 排序，命名 hot standby 添加的隐藏风险。

## A zh
- **Hot（active-active 或同步 active-passive）**：秒——standby 已经服务或有当前状态。代价 ~2 倍风险**split-brain**：两个节点相信它们是 primary，所以升级前你需要 fencing/quorum。
- **Warm**：分钟——副本运行但滞后；failover 丢失复制延迟窗口的写操作。
- **Cold**：小时——从备份恢复；数据丢失到上一个备份。
