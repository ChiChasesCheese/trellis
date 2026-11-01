---
id: hi-sd-youtube-8-resumable
node: sd.problem-breakdowns.youtube
type: qa
step: 8
---
## Q
**YouTube：断点续传**｜系统设计 · 问题拆解

YouTube 的大视频怎样支持断点续传？分块状态怎么记录，S3 事件通知在哪个环节触发？

## A
**与 Dropbox 同构。**
1. 客户端把文件切成约 5–10MB 的块，每块算指纹哈希
2. VideoMetadata 里有 chunks 字段，每项含指纹和状态；客户端先 POST 一次，把所有块登记为 NotUploaded
3. 客户端把每块传到 S3
4. S3 确认某个分块时返回分块号和 ETag，客户端用 `PATCH /videos/{id}/chunks` 转告后端，后端通过 S3 接口验证指纹或 ETag，再把对应块标记为 Uploaded
5. 中断后，客户端读取 VideoMetadata，看哪些块已传，跳过它们继续

**事件通知。** 客户端调用 CompleteMultipartUpload 后，S3 对该对象只发一次对象级通知，这个通知触发下游后处理；而分块级的进度仍由客户端驱动。

**说法。** 实际中这由 AWS multipart upload 处理，但面试里仍要讲清机制来体现深度。

**提醒。** 这里的续传指原始文件的上传进度，和后面的转码流水线不是一回事。
