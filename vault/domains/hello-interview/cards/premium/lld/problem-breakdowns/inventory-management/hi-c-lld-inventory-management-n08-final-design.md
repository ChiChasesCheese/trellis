---
id: hi-c-lld-inventory-management-n08-final-design
node: lld.problem-breakdowns.inventory-management.notes
type: qa
step: 8
---
## Q
**库存管理 · 最终类设计**｜摘要 · 必会

最终四块各负责什么？边界在哪？

## A
- **`InventoryManager`：** 在最上层做协调者，提供公共 API，路由到对应仓库；回答需要跨仓库的问题（哪些仓库能满足订单），协调多仓库操作（调拨）。
- **`Warehouse`：** 处理一个地点的库存。维护数量字典，强制"不能为负"，管理自己的告警配置，在阈值被穿越时通知；不知道其他仓库。
- **`AlertConfig`：** 阈值和监听器作为一个配置单元放在一起。
- **`AlertListener`：** 通知契约；实现负责实际投递。
- **分工的关键：** 每个部分有单一明确的职责，边界清楚：Manager 不碰库存数字，Warehouse 不认识别的仓库，告警的投递不在库存系统里。
