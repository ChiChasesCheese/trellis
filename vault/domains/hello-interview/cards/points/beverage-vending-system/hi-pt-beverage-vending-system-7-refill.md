---
id: hi-pt-beverage-vending-system-7-refill
node: qb.lld.beverage-vending-system.points
type: qa
step: 7
---
## Q
**多地点饮品自助售卖系统 · 补货通知与去重**｜追问 · 出自：多地点饮品自助售卖系统 › 逐步扩展 3

原料低于阈值要通知运维补货。用什么模式触发？怎么避免重复生成补货任务？

## A
**要点。** 观察者模式：库存是被观察者，每次 `commit` 后 `RefillMonitor` 检查水位，低于按原料配置的阈值（如牛奶低于 3 杯用量）就建任务并经 `Notifier` 通知。
**去重。** 同一机器同一原料只保留一个未完成任务（幂等），补货后水位恢复时关闭。
