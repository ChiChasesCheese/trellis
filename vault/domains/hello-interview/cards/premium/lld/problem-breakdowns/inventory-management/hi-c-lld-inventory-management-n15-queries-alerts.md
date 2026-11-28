---
id: hi-c-lld-inventory-management-n15-queries-alerts
node: lld.problem-breakdowns.inventory-management.notes
type: qa
step: 18
---
## Q
**库存管理 · 查询方法、设置告警与收集告警**｜摘要 · 追问

`get_stock`、`check_availability` 为什么也要加锁？`set_low_stock_alert`、`get_alerts_to_fire` 做什么？

## A
- **查询也加锁：** 为了看到一致的状态；没有同步的读可能因缺少内存屏障看到陈旧数据。更精细的做法（读写锁、volatile 字段）可用于读极多的场景，面试里主动说这个权衡，但默认用一致加锁最清楚。
- **`get_stock`：** 有则返回，没见过返回 0。
- **`check_availability`：** 数量为 0 或负数返回假，否则判断库存是否 ≥ 请求量。
- **`set_low_stock_alert`：** 校验阈值为正、监听器非空，在锁内取该商品的配置列表（没有就建空列表），追加新配置。多个告警自然支持。
- **`get_alerts_to_fire`：** 遍历该商品所有配置，对每个检查是否向下穿越（之前 ≥ 阈值且之后 < 阈值），收集要通知的监听器和上下文；只构建列表，不调用回调；没有则返回空。调用者（`remove_stock`）释放锁后触发。
- **配置对象不可变：** 创建后不改，重复通知的抑制靠穿越判断，不靠配置里的状态。
