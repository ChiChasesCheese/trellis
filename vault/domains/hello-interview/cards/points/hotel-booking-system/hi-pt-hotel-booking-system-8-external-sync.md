---
id: hi-pt-hotel-booking-system-8-external-sync
node: qb.sd.hotel-booking-system.points
type: qa
step: 8
---
## Q
**酒店预订系统 · 外部同步与乱序**｜追问 · 出自：酒店预订系统 › 整体设计

房态来自供应商的 webhook、API 推送和 30 分钟一次的转储，怎么保证 15 分钟内反映且不被乱序事件覆盖？

## A
**做法。** 推送先写 Kafka，规范化服务用「来源时间戳更晚才覆盖」更新库存与价格，旧事件丢弃；再产生事件刷新搜索摘要。转储做差异导入，只更新变化的行。
**新鲜度。** 大供应商以推送为主、拉取兜底，监控每个供应商的数据延迟。
