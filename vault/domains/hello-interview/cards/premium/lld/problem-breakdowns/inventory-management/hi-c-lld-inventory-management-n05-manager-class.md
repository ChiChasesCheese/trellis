---
id: hi-c-lld-inventory-management-n05-manager-class
node: lld.problem-breakdowns.inventory-management.notes
type: qa
step: 5
---
## Q
**库存管理 · InventoryManager 的状态与方法**｜摘要 · 必会

Manager 持有什么状态、暴露哪些方法？为什么 `add_stock` 没有返回值而 `remove_stock` 返回布尔？

## A
- **状态：** 一个"仓库 ID → 仓库"的字典。字典让按 ID 路由是 O(1)，也表达了"ID 对应仓库对象"的意思。ID 用字符串更灵活（`"DC_NY_01"` 这类有意义的标识），实际系统里 ID 也常来自外部。
- **方法与需求一一对应：**
  - `add_stock(warehouse, product, qty)`
  - `remove_stock(warehouse, product, qty) -> bool`
  - `transfer(product, from, to, qty) -> bool`
  - `warehouses_with(product, qty) -> list[str]`
  - `set_low_stock_alert(warehouse, product, threshold, listener)`
- **返回值的不对称是有意的：** 入库总能成功（总可以收更多货），所以不返回；出库可能因库存不足失败，调拨可能因库存不足或仓库 ID 无效失败，所以返回布尔。
- **构造：** 接收仓库 ID 列表，为每个建一个空仓库；仓库集合固定，所以不提供增删仓库的方法。
- **告警为什么不在 Manager 里管：** Manager 不知道具体商品，只知道仓库集合与可做的操作；它是对外 API，应简单专注。Warehouse 才是实际管库存的地方，告警配置由它持有，Manager 只路由。
