---
id: bagu-link-messenger-chat-system-1-map
node: links.messenger-chat-system
type: qa
step: 1
---
## Q
**聊天/即时通讯系统（WhatsApp / Messenger） · 会被追问哪些八股**｜必会

设计聊天/即时通讯系统（WhatsApp / Messenger）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 聊天难在收件人此刻连在哪台机器。基础是：epoll 撑起海量长连接、心跳判在线、WebSocket 推送、按会话分区保证会话内有序、序号加存储支撑断线补发。

**下钻路线。**
- 单机几十万长连接 → 不能一连接一线程，用 epoll 事件循环，[[a.net.epoll-io-models|I/O 多路复用与 epoll、Reactor、Java NIO]]
- 怎么知道用户在线 → 心跳超时判定，消息带长度字段防粘包，[[b.net.tcp-keepalive-sticky|TCP Keepalive、心跳、粘包与连接异常]]
- 消息怎么实时到对方 → WebSocket 全双工，不用轮询，[[a.net.websocket-push|消息推送]]
- 消息顺序怎么保证 → 按会话 ID 分区，只保证会话内有序，[[a.mq.ordering|消息顺序性怎么保证]]
- 消息 ID 怎么递增可排序 → 会话内单调序号，雪花 ID 要防时钟回拨，[[b.distributed.distributed-id|全局唯一 ID]]
- 断线重连消息不丢 → 会话内 seq 加服务端存储，客户端发现缺口补洞并去重，[[b.scenario.im-delivery|IM 与消息可靠下发]]
- 会话历史倒序翻页 → 联合索引 (会话, 时间) 的叶子链表反向扫描，[[a.mysql.bplus-tree|为什么 MySQL 索引用 B+ 树]]
- 网关发布时十万连接同时重连 → 随机退避，避免惊群，[[a.net.tcp-handshake|TCP 三次握手与四次挥手]]

**业务场景。** 抖音私信里用户在地铁中断网又恢复：按序号补发缺的几条，客户端按序号去重，不会漏也不会显示两遍。
**系统设计。** [[links.fb-live-comments|Facebook 直播评论]]：连接层相同，但评论可以采样丢弃，不必逐条补发；[[links.notification-system-scale|通知系统（支持单发与群发，百万级每秒）]]：群发也要按网关合并投递，但不要求会话内有序。
