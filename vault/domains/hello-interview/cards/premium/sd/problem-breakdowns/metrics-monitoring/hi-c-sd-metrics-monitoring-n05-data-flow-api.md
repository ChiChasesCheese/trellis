---
id: hi-c-sd-metrics-monitoring-n05-data-flow-api
node: sd.problem-breakdowns.metrics-monitoring.notes
type: qa
step: 5
---
## Q
**指标监控平台 · 数据流与接口**｜摘要 · 必会

指标监控平台的数据怎么端到端流动？三个核心接口怎么设计？

## A
- **数据流：** 服务产生指标并发给平台 → 平台摄入、校验并存成时序数据 → 用户通过仪表盘查询并聚合 → 告警规则被定期对已存数据评估 → 触发后通知到 Slack、PagerDuty、邮件。
- **三种特性：** 摄入和存储写多且持续（500 万点/秒）；查询读多且突发（工程师排障时）；告警评估和通知首先要可靠。这些差异驱动后面的设计。
- **摄入接口：** `POST /metrics/ingest`，体里是批量的 `{name, labels, value, timestamp}` 数组。批量发送是因为量大。
- **查询接口：** `GET /metrics/query?query=avg(cpu_usage{region="us-east"})&start=A&end=B&step=60`，返回时间戳数组和值数组。查询语言参照 PromQL，这是描述时序查询的典型 DSL。
- **告警规则接口：** `POST /alerts/rules`，体含名称、查询表达式（如 `avg(...) > 0.9`）、持续时间 `for: 5m`、通知目标。规则很少变，但被评估得极其频繁。
- **线上格式：** 示例用 JSON；这个规模下实际会用 protobuf 这类二进制格式，说一句即可。
