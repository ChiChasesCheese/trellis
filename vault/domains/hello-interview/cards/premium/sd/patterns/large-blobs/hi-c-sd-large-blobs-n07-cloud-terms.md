---
id: hi-c-sd-large-blobs-n07-cloud-terms
node: sd.patterns.large-blobs.notes
type: qa
step: 14
---
## Q
**大文件 · 三大云的术语对照**｜摘要 · 加分

AWS、Google Cloud、Azure 分别怎么叫这些概念？需要背吗？

## A
- **临时上传 URL：** AWS 预签名 URL（PUT 或 POST）；Google 签名 URL（可续传或简单）；Azure SAS 令牌（Shared Access Signature）。
- **分块上传：** AWS Multipart Upload（分块 5MB 到 5GB）；Google Resumable Uploads（块大小灵活）；Azure Block Blobs（块大小灵活，新版本单块最大约 4000 MiB）。
- **事件通知：** AWS S3 事件通知（到 Lambda、SQS、SNS）；Google Cloud Storage 的 Pub/Sub（到 Cloud Functions）；Azure Event Grid。
- **带签名的 CDN：** AWS CloudFront 签名 URL 或 Cookie；Google Cloud CDN 签名 URL；Azure CDN 的 SAS 令牌。
- **清理策略：** AWS 生命周期规则；Azure 生命周期管理策略；Google 生命周期管理。
- **面试怎么处理：** SDK 的函数和参数名不需要背，理解主意就行；被问到某家的对应物时能说出上表即可。
