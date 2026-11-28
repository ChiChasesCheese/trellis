---
id: hi-c-lld-inventory-management-n06-warehouse-class
node: lld.problem-breakdowns.inventory-management.notes
type: qa
step: 6
---
## Q
**库存管理 · Warehouse 的状态与方法**｜摘要 · 必会

Warehouse 要存什么？为什么每个商品的告警配置是一个列表？

## A
- **状态三项：** `id`（告警回调要告诉监听器是哪个仓库）；`inventory`（商品 ID → 数量，没出现过的商品默认 0，不必预先初始化）；`alertConfigs`（商品 ID → 告警配置列表）。
- **为什么是列表：** 一个商品可有多个告警：库存到 50 发邮件提醒补货，到 10 呼叫值班。不同阈值可触发不同渠道、发给不同团队。多数商品只有 0 或 1 个，列表不增加复杂度。要不要支持多告警值得和面试官确认。
- **方法：** `add_stock`、`remove_stock -> bool`、`get_stock`、`check_availability`、`set_low_stock_alert`；外加私有的 `get_alerts_to_fire(product, previous, new)`。
- **私有辅助：** 在 `remove_stock` 里被调用，检查该商品的配置哪些阈值被穿越，返回要通知的监听器；调用方在释放锁之后再触发。
- **库存检查与告警的归属：** 不能为负的规则、告警配置、触发都归 Warehouse，它不需要知道其他仓库。
