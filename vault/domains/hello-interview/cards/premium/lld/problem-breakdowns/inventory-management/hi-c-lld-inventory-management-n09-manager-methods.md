---
id: hi-c-lld-inventory-management-n09-manager-methods
node: lld.problem-breakdowns.inventory-management.notes
type: qa
step: 9
---
## Q
**库存管理 · Manager 的简单方法与校验**｜摘要 · 必会

`add_stock`、`remove_stock`、`warehouses_with`、`set_low_stock_alert` 的实现和失败行为是什么？

## A
- **构造：** 遍历仓库 ID 列表，为每个建空仓库（无库存、无告警）存进字典。
- **`add_stock`：** 查仓库，不存在就快速失败抛错；然后委托仓库入库。校验过仓库之后入库总是成功。
- **`remove_stock`：** 查仓库，不存在返回 `False`；否则返回仓库给的布尔值，让调用方知道是否成功。注意与 `add_stock` 对未知仓库的处理不同（抛错 vs 返回假），要选定立场并保持一致。
- **`warehouses_with`：** 遍历所有仓库，问每个"够不够"，收集够的 ID；可能是空列表。
- **`set_low_stock_alert`：** 告警是仓库的属性，查到仓库后委托给它，仓库不存在抛错。
- **边界：** 数量为 0 或负数的入库、出库直接拒绝；阈值要为正，监听器不能为空；这些校验放在最终持有状态的 Warehouse 里。
- **一个提醒：** `warehouses_with` 逐个仓库加锁读，得到的是各时刻的快照，不是全局一致的结果，只能当参考。
