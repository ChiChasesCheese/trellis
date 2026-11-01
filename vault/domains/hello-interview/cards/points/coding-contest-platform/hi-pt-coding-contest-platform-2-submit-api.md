---
id: hi-pt-coding-contest-platform-2-submit-api
node: qb.sd.coding-contest-platform.points
type: qa
step: 2
---
## Q
**在线判题与编程竞赛平台 · 提交接口与信任边界**｜出自：在线判题与编程竞赛平台 › 核心实体与接口

`POST /problems/{id}/submit` 的请求体里放什么？用户 ID 和时间戳从哪里来？客户端怎么拿到结果？

## A
**要点。** 请求体只有 `code` 和 `language`；用户 ID 来自登录态，时间戳由服务端生成，不信任客户端传入的身份与时间。返回 submission_id。
**结果。** 客户端每秒轮询 `GET /submissions/{id}` 直到状态为 DONE。
