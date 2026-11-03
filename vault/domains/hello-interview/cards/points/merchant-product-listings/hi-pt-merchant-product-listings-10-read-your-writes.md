---
id: hi-pt-merchant-product-listings-10-read-your-writes
node: qb.sd.merchant-product-listings.points
type: qa
step: 10
---
## Q
**商家商品上架与更新系统 · 商家读自己的写**｜追问 · 出自：商家商品上架与更新系统 › 深入 4

商家改完价格刷新后台，却读到旧值，以为没成功。怎么解决？普通用户需要同样保证吗？

## A
**方案。** 商家后台读主库；或响应带版本号，读路径要求版本不低于该值，缓存不满足则回源。
**用户。** 普通用户读最终一致即可。
