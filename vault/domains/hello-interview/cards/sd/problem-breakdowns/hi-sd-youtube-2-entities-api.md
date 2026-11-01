---
id: hi-sd-youtube-2-entities-api
node: sd.problem-breakdowns.youtube
type: qa
step: 2
---
## Q
**YouTube：实体与接口演化**｜系统设计 · 问题拆解

YouTube 的核心实体是什么？上传和播放接口一开始怎么定义，后来为什么要改？

## A
**实体。** User（上传者或观看者）、Video（被上传和观看的视频）、VideoMetadata（上传者、字幕链接等元数据）。

**最初的接口。**
- `POST /upload`：请求体包含 Video 和 VideoMetadata
- `GET /videos/{videoId}`：返回 Video 与 VideoMetadata

**后来的改动。**
- 因为要让客户端用预签名 URL 直传对象存储，上传改为 `POST /presigned_url`，请求只带元数据，不带视频文件
- 播放时视频内容放在 S3，GET 只返回 VideoMetadata，里面含有播放所需的 URL（清单文件地址）

**说法。** 一开始就说明「我先给简单接口，深入后可能回头改」，因为上传和播放接口在权衡方案后会大幅演化。
