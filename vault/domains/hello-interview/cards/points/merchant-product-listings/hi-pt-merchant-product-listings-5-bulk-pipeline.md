---
id: hi-pt-merchant-product-listings-5-bulk-pipeline
node: qb.sd.merchant-product-listings.points
type: qa
step: 5
---
## Q
**商家商品上架与更新系统 · 批量任务的拆分与处理**｜出自：商家商品上架与更新系统 › 整体设计

商家上传了几十万行文件，系统怎样拆分并保证同一商品的更新有序？进度和错误怎么汇报？

## A
**拆分。** 拆分任务按固定行数（如 500 条）切片，每片一条 Kafka 消息，键是 `productId`，同商品进同一分区、保持顺序。
**处理。** Worker 逐条校验写主库，成功与失败分别计数，失败行连同原因追加到错误文件，任务状态由计数推出。
**幂等。** 行级别幂等重试；死信队列保存反复失败的分片。
