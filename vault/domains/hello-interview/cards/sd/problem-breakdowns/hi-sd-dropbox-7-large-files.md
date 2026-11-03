---
id: hi-sd-dropbox-7-large-files
node: sd.problem-breakdowns.dropbox.exam
type: qa
step: 7
---
## Q
**Dropbox：为什么 50GB 文件需要分块**｜系统设计 · 问题拆解

Dropbox 要支持 50GB 的大文件，为什么不能用一次 POST 上传？分块（chunking）要在哪一端做、怎样记录进度？

## A
**单次 POST 的问题。**
- 超时：50GB × 8 位 ÷ 100Mbps = 4000 秒，约 1.1 小时，请求会超时
- 限制：浏览器和服务端常限制请求体，Amazon API Gateway 硬限制只有 10MB
- 网络中断：断线要从头来过
- 体验：用户看不到进度

**做法。** 客户端把文件切成 5–10MB 的块，逐个或并行上传，可按网络状况调整块大小。块越小，进度条越细，断点续传越便宜。

**易错。** 必须在客户端分块。在服务端分块等于文件已经整个传上来了，白白失去意义。

**续传状态。** 在 FileMetadata 里加 chunks 数组，记录每块状态（uploaded / uploading / not-uploaded）。续传时读它，只传没传完的块。
