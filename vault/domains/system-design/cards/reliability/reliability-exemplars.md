---
id: reliability-exemplars
node: reliability.observability
type: qa
---
## Q
You see a p99 latency spike on a dashboard and now need one concrete slow request to debug. What feature jumps you straight from the metric to a trace, and how does it work?

## A
**Exemplars**: when recording a latency observation into a histogram bucket, the metrics SDK attaches the current **trace ID** (a sampled reference request) to that bucket. The dashboard renders exemplars as clickable points on the latency chart — one click lands on a real trace from the slow bucket.

This closes the classic gap: metrics tell you *that/where* it's slow, traces tell you *why*, and exemplars are the join between them — no timestamp archaeology across systems. Requires trace context active where metrics are recorded (OpenTelemetry does this natively).

## Q zh
你在仪表板上看到 p99 延迟峰值，现在需要一个具体的慢请求来调试。什么功能直接从指标跳到跟踪，它是如何工作的？

## A zh
**Exemplar**：将延迟观测记录到直方图桶时，指标 SDK 附加当前**追踪 ID**（一个采样引用请求）到该桶。仪表板呈现 exemplar 作为延迟图表上的可点击点——一次点击登陆一个真实跟踪来自慢桶。

这关闭经典差距：指标告诉你*那/哪里*慢，跟踪告诉你*为什么*，exemplar 是它们之间的连接——无跨系统的时间戳考古。需要追踪上下文活跃在指标被记录的地方（OpenTelemetry 本地做这个）。
