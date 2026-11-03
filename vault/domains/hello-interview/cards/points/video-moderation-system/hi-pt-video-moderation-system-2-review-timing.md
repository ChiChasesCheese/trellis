---
id: hi-pt-video-moderation-system-2-review-timing
node: qb.sd.video-moderation-system.points
type: qa
step: 2
---
## Q
**视频内容审核系统 · 先审后发还是先发后审**｜必会 · 出自：视频内容审核系统 › 整体设计

视频审核系统里，审核和发布的先后是什么取舍？

## A
**先审后发。** 最安全，但延迟直接影响用户体验。
**常见做法。** 先发布（限制分发）并并行审核；高风险的新账号或敏感内容可以先审后发。
**接入。** 视频服务发 VideoPublished 事件到 Kafka，按 videoId 分区；大文件只传对象存储引用。
