---
id: hi-c-sd-instagram-b04-s3-multipart-facts
node: sd.problem-breakdowns.instagram.beyond
type: qa
step: 4
---
## Q
**Instagram 图片分享 · 拓展：S3 分片上传的实际限制与坑**｜拓展 · 加分

S3 multipart upload 有哪些硬限制？分片上传中途放弃会怎样？预签名 URL 怎么配合分片？

## A
- **限制：** 每片 5MiB–5GiB（最后一片可小于 5MiB），最多 10,000 片，单个对象最大 48.8 TiB（2025 年 12 月前是 5 TiB）。所以 4GiB 的视频用 64MiB 一片只需 64 片，远在限制内。
- **中止的上传会一直占费：** 已上传的片即使没完成合并也按存储计费，直到手动中止；应在桶上配置生命周期规则，自动清理超过 N 天仍未完成的分片上传。
- **预签名 URL：** 每一片需要各自的预签名 URL（CreateMultipartUpload 返回 uploadId，然后给每个 partNumber 签名一个 URL），客户端并行传各片，最后调用 CompleteMultipartUpload 并带上各片的 ETag 列表。
- **完整性：** 客户端失败可只重传失败的那片，所以断点续传的粒度是一片，片越小越灵活但请求次数越多。
- **取舍：** 片大小决定并行度、重试代价与请求数；10,000 片的上限也限制了最小片大小，视频越大片越不能太小。
