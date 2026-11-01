---
id: hi-pt-feature-flags-service-9-governance
node: qb.sd.feature-flags-service.points
type: qa
step: 9
---
## Q
**功能开关服务 · 控制面治理**｜出自：功能开关服务 › 深入 4

生产环境的开关变更要有哪些安全与治理措施？

## A
**要点。** 角色权限，重要开关双人审批；变更写审计、一键回滚到上个版本；环境隔离（开发/预发/生产）；定时放量（凌晨 5% 升到 25%）并设护栏，错误率或延迟恶化自动回退；开关记录责任人和过期时间，用完必须清理。
