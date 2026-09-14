---
id: access-history-latency-retention
node: security.data-lineage-and-access-history
type: qa
tags: [grown]
---
## Q
安全团队想用 `ACCESS_HISTORY` 做实时告警（某人刚读了薪资表就报警），为什么不太合适？

## A
`ACCESS_HISTORY` 位于 ACCOUNT_USAGE 共享库中，数据有延迟（可能长达约 3 小时）才出现，因此适合事后审计与定期巡检，而不是秒级实时告警；它保留约一年历史，适合合规回溯。另外它需要 Enterprise 及以上版本。实时性要求高的场景应在访问入口处用行级访问策略或脱敏策略做预防性控制，而非依赖事后日志。
