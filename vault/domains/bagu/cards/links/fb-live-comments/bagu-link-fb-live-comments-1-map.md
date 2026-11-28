---
id: bagu-link-fb-live-comments-1-map
node: links.fb-live-comments
type: qa
step: 1
---
## Q
**Facebook 直播评论 · 会被追问哪些八股**｜必会

设计Facebook 直播评论时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 写入、存储、推送三条线用 MQ 解耦。基础是：epoll 撑百万长连接、WebSocket、有缓冲 channel 隔离慢消费者、大 key 与热点 key、洪峰削峰。

**下钻路线。**
- 评论系统整体怎么分 → 写入、存储、推送三条线，用 MQ 解耦，[[a.scenario.live-comment|直播间评论、弹幕与点赞的高并发设计]]
- 评论实时展示用什么协议 → WebSocket，握手走 HTTP，网关配升级头和空闲超时，[[a.net.websocket-push|消息推送]]
- 开播瞬间百万长连接 → epoll 事件循环，读半条消息要保留缓冲，ET 读到 EAGAIN，[[a.net.epoll-io-models|I/O 多路复用与 epoll、Reactor、Java NIO]]
- 评论广播给观众 → 每连接一个有缓冲 channel，满了丢弃或断开，不拖累广播，[[b.runtime.go-channel-map|Go 的 channel 实现、select 与 map 并发安全]]
- 一个直播间的评论放一个 key → 只缓存最新一两页，按时间分段，[[b.cache.big-key|大 key 的危害与处理]]
- 热门直播间读取全落一个 key → 本地缓存，副本分流，[[a.cache.hot-key|热 key 的发现与处理]]
- 评论洪峰 → 队列削峰，积压时旧评论可以不再展示，[[a.protect.spike-10x|QPS 突增 10 倍怎么应对]]

**业务场景。** 抖音直播间开播瞬间，百万观众涌入拉评论和弹幕：评论可以采样丢弃，礼物却一条都不能丢。
**系统设计。** [[links.messenger-chat-system|聊天/即时通讯系统（WhatsApp / Messenger）]]：连接层相同，但聊天要逐条送达并补发；[[links.notification-system-scale|通知系统（支持单发与群发，百万级每秒）]]：群发同样按网关合并投递。
