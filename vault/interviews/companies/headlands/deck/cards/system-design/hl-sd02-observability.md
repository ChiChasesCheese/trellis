---
id: hl-sd02-observability
node: system-design.sd02-job-scheduler
type: qa
step: 29
---
## Q
调度器要监控哪些指标？各自告警阈值是什么？

## A
- **`lateness = actualFire − fireAt` 的直方图**（p50 / p99 / p99.9 / max，按租户）：直接度量 SLO，告警 p99.9 > Δ/2；
- 到期未分发积压数 / 年龄最大值：突发或下游慢的早期信号，告警年龄 > Δ；
- WAL 提交延迟、复制滞后（follower lag）：写路径与热备健康，滞后 > 1 s 告警；
- 时间轮大小、装载器滞后：近期窗口是否准备好，装载滞后 > 窗口/2 告警；
- 时钟偏移：防止早发，> ε_max/2 告警；
- epoch 变化、fencing 拒绝次数：选主抖动，任何拒绝都告警；
- 死信数量：下游长期失败，> 0 告警。
