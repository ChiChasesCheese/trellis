---
id: hi-pt-merchant-product-listings-11-tombstone-shard
node: qb.sd.merchant-product-listings.points
type: qa
step: 11
---
## Q
**商家商品上架与更新系统 · 下架墓碑与分片键**｜出自：商家商品上架与更新系统 › 取舍与追问

商品下架或删除时怎样避免被迟到的旧更新复活？主库按什么分片，商家后台列表怎么查？

## A
**墓碑。** 下架用墓碑（tombstone）事件，同样带版本，保证删除不被迟到旧更新复活。
**分片。** 主库按 `productId` 哈希分片分散热点；商家后台列表需 `merchantId` 的二级索引（全局索引，或单独的商家维度投影表）。
**图片。** 图片拉取与缩放走独立异步流水线，商品先以占位图上线。
