---
id: hi-ov-fb-live-comments-3-when
node: sd.problem-breakdowns.fb-live-comments
type: qa
step: 3
tags: [通览]
---
## Q
**直播评论 · 深挖清单**｜通览

直播评论会被追问哪些深挖？各自的做法和代价是什么？

## A
- **实时推送：** 用 SSE 单向推送，发评论仍走 POST；读远多于写，WebSocket 为每个观众开双向通道开销大；代理可能缓冲，浏览器限制并发连接数。
- **规模扩展：** 拆出实时消息服务器，按 hash(liveVideoId) 分频道的 pub/sub，L7 负载均衡按直播一致性哈希让同一直播的观众落同一台，或用调度服务；朴素 pub/sub 每台处理所有评论太浪费；要同步订阅与路由。爆红直播先采样，再改 CDN 每秒快照，延迟 1 到 2 秒。
- **断线重连：** SSE 的 Last-Event-ID 重连时回放错过的评论，客户端也记最后评论 ID 去补；用户不会漏评论；只回放近 5 分钟，换服务器要共享 Redis 缓存，还要去重合并。

**各级别。** 中级看出轮询的局限并想到推送和 pub/sub；高级主导扩展并比较取舍；Staff 点出 pub/sub 的局限，并想到超级直播要改需求。
