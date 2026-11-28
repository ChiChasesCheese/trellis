---
id: bagu-link-online-chess-platform-1-map
node: links.online-chess-platform
type: qa
step: 1
---
## Q
**在线国际象棋平台 · 会被追问哪些八股**｜必会

设计在线国际象棋平台时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 一局棋是小而强一致的状态机，走棋必须可靠有序。基础是：TCP 与 WebSocket 的选型、事件循环与业务线程分离、重连的序号、CPU 密集任务隔离、GC 停顿对计时的影响。

**下钻路线。**
- 走棋用 WebSocket 还是 UDP → 每步必须可靠有序，用 TCP；QUIC 只改善弱网切换，[[b.net.tcp-udp-quic|TCP 与 UDP 的区别、QUIC 是什么]]
- 一步棋怎么同步给双方 → I/O 线程只收发编解码，走棋校验交业务线程，[[a.net.epoll-io-models|I/O 多路复用与 epoll、Reactor、Java NIO]]
- 玩家断线重连 → 旧报文不会污染新连接，应用层按走棋序号去重，[[a.net.tcp-handshake|TCP 三次握手与四次挥手]]
- 引擎分析与实时通信同进程 → 隔离 CPU 密集任务，靠抢占式调度，[[a.runtime.go-gmp|Go 的 GMP 调度模型]]
- GC 停顿会影响计时公平吗 → 计时以服务端为准，选低停顿收集器，[[a.runtime.java-gc-fullgc|JVM 垃圾回收]]
- 按 Elo 匹配 → 按分数范围取近邻，等待越久范围越宽，棋钟由服务端裁定并补偿有上限的延迟，[[b.scenario.matchmaking-clock|匹配与服务端时钟]]

**业务场景。** 抖音直播的连麦 PK：双方分数实时同步，网络断了重连后必须回到正确比分，不能重复加分。
**系统设计。** [[links.messenger-chat-system|聊天/即时通讯系统（WhatsApp / Messenger）]]：同样的长连接和重连补发，但棋局有唯一写者与服务端计时；[[links.realtime-game-leaderboard|在线游戏排行榜（全球榜 + 我的名次 + 好友榜）]]：Elo 排名同样用 ZSet。
