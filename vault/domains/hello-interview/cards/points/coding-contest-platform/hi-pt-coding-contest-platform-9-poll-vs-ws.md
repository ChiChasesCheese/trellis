---
id: hi-pt-coding-contest-platform-9-poll-vs-ws
node: qb.sd.coding-contest-platform.points
type: qa
step: 9
---
## Q
**在线判题与编程竞赛平台 · 轮询还是 WebSocket**｜追问 · 出自：在线判题与编程竞赛平台 › 取舍与追问

追问：为什么用轮询而不是 WebSocket 推判题结果？

## A
**取舍。** 轮询间隔 1 秒，10 万用户同时等待也只是约 10 万次/秒的轻量读（DONE 状态走缓存或键值查询）。
**为什么不推。** WebSocket 要维护十万级长连接，复杂度更高，收益只有不到一秒的延迟。
