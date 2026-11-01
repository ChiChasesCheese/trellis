---
id: hi-pt-stock-price-alerts-4-conflation
node: qb.sd.stock-price-alerts.points
type: qa
step: 4
---
## Q
**股票价格提醒系统 · 合并与分区**｜出自：股票价格提醒系统 › 整体设计

股价提醒系统每只活跃股票每秒数十次更新。判断节点怎么减少无用计算又不漏报？

## A
**分区。** Kafka 按 symbol 分区，保证同一只股票更新有序。
**合并（conflation）。** 每只股票只保留最新价，按固定周期（如 100 毫秒）处理一次。
**不漏报。** 判断针对当前价的范围查询，中间被越过的阈值不会漏；价格跳空同时穿越多个阈值也一次取出，各自触发。
