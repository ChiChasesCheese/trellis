---
id: hi-pt-kv-store-eviction-11-switch-granularity
node: qb.lld.kv-store-eviction.points
type: qa
step: 11
---
## Q
**可配置淘汰策略的内存键值存储 · 运行时切换策略与淘汰粒度**｜加分 · 出自：可配置淘汰策略的内存键值存储 › 取舍与追问

追问：淘汰策略怎么在运行时切换？多种数据结构共用一个策略合理吗？

## A
**切换。** 策略只持有元数据，用现有键重建新策略对象（对全部键重新 `on_insert`），代价是丢失访问历史。
**粒度。** 淘汰粒度是 key，不是元素，大集合里的某个元素不会被单独淘汰。
