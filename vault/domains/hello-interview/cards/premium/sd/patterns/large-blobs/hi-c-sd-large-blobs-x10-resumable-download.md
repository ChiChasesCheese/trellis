---
id: hi-c-sd-large-blobs-x10-resumable-download
node: sd.patterns.large-blobs.exam
type: qa
step: 10
---
## Q
**大文件 · 5GB 下载中途断线**｜考点 · 必会

用户下载 5GB 文件，连接断了。怎么支持续传？

## A
- **范围请求：** 用 `Range: bytes=start-end` 只请求某段，客户端记录已完成范围，重连后请求缺失部分。
- **前提：** 存储和 CDN 支持（都支持），签名 URL 不限制所需的 HTTP 动词和头。
- **浏览器和下载管理器：** 自动处理续传。
- **加速：** 一般不需要并行分块；只在分发多 GB 文件且用户抱怨速度时才考虑，通常用户受总带宽限制而不是单连接。
