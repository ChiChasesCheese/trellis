---
id: hi-pt-merchant-product-listings-4-optimistic-version
node: qb.sd.merchant-product-listings.points
type: qa
step: 4
---
## Q
**商家商品上架与更新系统 · 单条更新的乐观并发**｜必会 · 出自：商家商品上架与更新系统 › 整体设计

商家单条更新商品时怎样处理并发修改？校验放在哪里？

## A
**机制。** 带版本做乐观并发控制：`UPDATE ... WHERE id=? AND version=?`，不一致返回 409，商家刷新后重试；成功版本加一，数据库提交即向商家确认。
**校验。** 入口做格式校验（价格非负、类目合法、长度），批量时 Worker 做业务校验，不合格行进错误文件，而不是让整个任务失败。
