---
id: hi-sd-fb-live-comments-1-requirements
node: sd.problem-breakdowns.fb-live-comments.exam
type: qa
step: 1
---
## Q
**直播评论的需求与接口**｜系统设计 · 题目拆解

设计 Facebook 直播评论（Live Comments）：观众能在直播视频下发评论，实时看到别人的新评论，也能看到加入之前的历史评论。请说明核心功能与非功能需求（含数字）、核心实体和两个接口。

## A
**功能。** 发评论；观看时实时看到新评论；加入时能看到更早的评论。回复和点赞划到范围外。

**非功能。** 支持百万级并发直播、单个直播每秒数千条评论；可用性优先于一致性（最终一致即可）；端到端延迟小于 200 ms（人对 200 ms 内的反馈感觉是即时的）。鉴权与内容审核划到范围外。

**实体。** 用户（User）、直播视频（Live Video，由别的团队负责，只需对接）、评论（Comment）。

**接口。** `POST /comments/:liveVideoId`，请求体只有 message；用户 ID 不放在请求体里，而是从请求头的 JWT 或会话令牌里解析，防止冒充。`GET /comments/:liveVideoId?cursor=...&pageSize=10&sort=desc` 取历史评论。
