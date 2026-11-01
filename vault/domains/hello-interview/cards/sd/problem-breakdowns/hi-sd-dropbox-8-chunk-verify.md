---
id: hi-sd-dropbox-8-chunk-verify
node: sd.problem-breakdowns.dropbox
type: qa
step: 8
---
## Q
**Dropbox：分块状态如何可信同步**｜系统设计 · 问题拆解

Dropbox 分块上传中，chunks 状态靠客户端 PATCH 更新有什么风险？怎样做服务端校验，又怎样用指纹（fingerprint）判断一个文件是否传过？

## A
**只信客户端的风险。** 恶意客户端可以不上传就把所有块标成 uploaded，造成难以排查的不一致状态（只会损坏自己的文件，但仍是隐患）。

**做法：信任但校验（trust but verify）。** 每块上传后 S3 返回 ETag，客户端把 ETag 通过 PATCH 报给后端，后端用 S3 的 ListParts 批量核对，再改 chunks 状态。S3 事件通知只在整个分段上传完成时触发，单个分块不会触发，所以必须自己调用 ListParts。

**指纹。** 对文件内容做 SHA-256 得到指纹，不依赖文件名，因为不同用户可能同名。指纹用于去重和判断能否续传；fileId 仍用 UUID，指纹单独存一个字段。每个块也有自己的指纹。

**流程。** 先查同指纹且为 uploading 的记录，有就续传；没有就调 CreateMultipartUpload 拿 uploadId，给每块发预签名 URL；全部块确认后调 CompleteMultipartUpload，成功才把文件状态改为 uploaded。
