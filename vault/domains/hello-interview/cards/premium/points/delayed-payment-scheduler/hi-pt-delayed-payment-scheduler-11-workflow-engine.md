---
id: hi-pt-delayed-payment-scheduler-11-workflow-engine
node: qb.sd.delayed-payment-scheduler.points
type: qa
step: 11
---
## Q
**延迟支付调度服务 · 工作流引擎的取舍**｜加分 · 出自：延迟支付调度服务 › 深入 7

能否用工作流引擎（如 Temporal）的定时器代替自建数据库扫描器来做延迟转账？利弊是什么？

## A
**好处。** 持久化定时器和重试开箱即用，流程复杂（多步审批）时省力。

**代价。** 假设 1,000 万条预约同时在途，就是 1,000 万个长期工作流，成本高；资金状态仍要放进数据库。

**取舍。** 预约量小、流程复杂选引擎；量大、流程简单选数据库加扫描。
