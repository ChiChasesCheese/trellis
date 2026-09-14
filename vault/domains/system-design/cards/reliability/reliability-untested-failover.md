---
id: reliability-untested-failover
node: reliability.multi-region
type: qa
---
## Q
Why does an untested regional failover "not exist," and what two practices make failover real?

## A
Failover paths rot silently: the standby region drifts (missing config, stale capacity quotas, expired secrets, un-replicated new dependencies), and the first execution under pressure discovers all of it at once. A DR plan that has never run is a hypothesis, not a capability.

- **Regular game days / DR drills**: fail over real (or shadow) traffic on a schedule and measure actual RTO/RPO against the objectives.
- **Continuous validation**: standby capacity provisioned and health-checked, runbooks executable by automation, ideally routine traffic served from the secondary so drift surfaces immediately.

## Q zh
为什么未测试的区域故障转移"不存在，"什么两个做法使故障转移真实？

## A zh
故障转移路径静音腐烂：备用区域漂移（缺少配置、陈旧容量配额、过期密钥、未复制新依赖），在压力下的第一次执行一次发现所有。从未运行的 DR 计划是假设，不是能力。

- **定期游戏日 / DR 演练**：按计划故障转移真实（或影子）流量并测量实际 RTO/RPO 对目标。
- **持续验证**：备用容量已配置和健康检查，可执行的自动化的剧本，理想情况下常规流量从辅助服务所以漂移立即浮出。
