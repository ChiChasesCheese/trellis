---
id: hi-pt-video-moderation-system-5-task-idempotency
node: qb.sd.video-moderation-system.points
type: qa
step: 5
---
## Q
**视频内容审核系统 · 审核任务幂等**｜出自：视频内容审核系统 › 深入 1

视频审核收到重复的发布事件或视频被编辑，怎么避免重复审核或沿用旧结论？

## A
**任务键。** videoId + 版本，重复事件不会产生第二次审核。
**编辑。** 视频被编辑则版本递增，旧结论失效。
**升级。** 传播量突增的老视频触发重新审核。
