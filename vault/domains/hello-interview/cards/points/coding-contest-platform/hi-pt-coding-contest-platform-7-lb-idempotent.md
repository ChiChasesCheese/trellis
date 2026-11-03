---
id: hi-pt-coding-contest-platform-7-lb-idempotent
node: qb.sd.coding-contest-platform.points
type: qa
step: 7
---
## Q
**在线判题与编程竞赛平台 · 榜单幂等与读缓存**｜追问 · 出自：在线判题与编程竞赛平台 › 深入 4

判题 worker 重试会重复上报同一结果，榜单为什么不能用 `ZINCRBY`？10 万人轮询榜单的读压力怎么扛？

## A
**幂等。** 不用 `ZINCRBY`，而是按数据库里该用户每题首次通过记录重算分数，再 `ZADD` 覆盖。
**读压力。** 10 万人每 5 秒刷新约 2 万次/秒；前 100 名在应用内存或 CDN 缓存 1～2 秒，所有人共享同一份，个人名次再单独 `ZREVRANK`。
