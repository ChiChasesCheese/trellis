---
id: hi-sd-key-technologies-2-blob-storage
node: sd.in-a-hurry.key-technologies.exam
type: qa
step: 2
---
## Q
**对象存储（Blob Storage）的用法**｜系统设计 · 速览

什么时候该用对象存储而不是数据库存数据？标准的上传下载流程是什么？面试里要知道它的哪些特性？

## A
**用在哪。** 图片、视频、文件这类大的非结构化数据（YouTube、Instagram、Dropbox）。放进数据库既贵又低效。典型结构是：核心数据库（Postgres / DynamoDB）只存元数据和指向 blob 的指针，blob 放 S3 / GCS，前面常配 CDN。除非有很好的理由，不要把 S3 当主数据库。

**标准流程。**
- 上传：客户端向服务器要预签名 URL（presigned URL），直接上传到对象存储；对象存储完成后通知服务器，更新状态
- 下载：服务器返回预签名 URL，客户端经 CDN 下载

**要知道的特性。**
- 持久性：靠复制和纠删码（erasure coding）
- 扩展性：可视为无限，不必讨论
- 成本：S3 约 0.023 美元 / GB / 月，而 DynamoDB 约 0.25 美元 / GB / 月，约相差 10 倍
- 安全：静态和传输加密、访问控制
- 分块上传：S3 的 multipart upload 支持断点续传和并行

**选择。** 不熟时选 S3，其他厂商也多有 S3 兼容接口。
