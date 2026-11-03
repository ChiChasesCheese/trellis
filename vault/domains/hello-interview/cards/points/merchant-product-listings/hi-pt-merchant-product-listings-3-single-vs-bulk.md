---
id: hi-pt-merchant-product-listings-3-single-vs-bulk
node: qb.sd.merchant-product-listings.points
type: qa
step: 3
---
## Q
**商家商品上架与更新系统 · 单条同步与批量异步**｜必会 · 出自：商家商品上架与更新系统 › 核心实体与接口

商家的单条更新和批量更新为什么采用不同的处理方式？批量接口怎么设计才能避免大文件占用应用服务器？

## A
**单条。** 同步写主库，带 `If-Match: version`，商家要即时反馈。
**批量。** 异步：`POST /bulk-jobs` 返回预签名上传地址和 jobId，商家直传对象存储后 `start`，`GET /bulk-jobs/{id}` 查进度和逐行错误文件。量大、需要逐行报告。
