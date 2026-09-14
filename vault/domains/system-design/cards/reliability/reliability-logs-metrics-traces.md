---
id: reliability-logs-metrics-traces
node: reliability.observability
type: qa
---
## Q
Logs, metrics, traces: which one answers "is it broken?", "where is it broken?", and "why is this request broken?" — and what does each cost at scale?

## A
- **Metrics** → "is it broken?": pre-aggregated time series; cheap to store and alert on, but you can only ask questions you pre-declared.
- **Traces** → "where?": follow one request across services, showing which hop ate the latency; cost controlled by sampling.
- **Logs** → "why?": arbitrary per-event detail for the specific failing case; the most expensive per event — volume scales with traffic, so structured + sampled or they dominate infra cost.

## Q zh
日志、指标、跟踪：哪个回答"它坏了吗？"、"它在哪里坏了？"和"为什么这个请求坏了？"——每个在规模上的代价是什么？

## A zh
- **Metrics** → "是否坏？"：预聚合时间序列；便宜存储和告警，但你只能问你预先声明的问题。
- **Traces** → "哪里？"：跟随一个请求跨服务，显示哪个 hop 吃了延迟；成本由采样控制。
- **Logs** → "为什么？"：任意每事件细节为特定失败情况；最昂贵的每事件——体积与流量成比例，所以结构化 + 采样或它们主导基础设施成本。
