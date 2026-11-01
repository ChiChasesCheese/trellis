---
id: hi-pt-merchant-product-listings-6-cdc
node: qb.sd.merchant-product-listings.points
type: qa
step: 6
---
## Q
**商家商品上架与更新系统 · 用 CDC 避免双写**｜出自：商家商品上架与更新系统 › 整体设计

商品写入主库后，还要更新缓存、搜索索引并通知下游。为什么不在代码里同时写库和发消息？

## A
**问题。** 双写会出现写库成功、发消息失败。
**做法。** 主库提交后由变更数据捕获（CDC）产生 `ProductEvent` 发往 Kafka，三类消费者：缓存更新者、搜索索引器、下游业务（推荐、价格提醒）。
**修复。** 事件流可回放，用于对账和修复索引。
