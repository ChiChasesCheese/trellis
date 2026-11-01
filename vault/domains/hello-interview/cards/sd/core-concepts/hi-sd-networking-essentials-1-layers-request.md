---
id: hi-sd-networking-essentials-1-layers-request
node: qb.sd.messenger-chat-system.pre-sd-core-concepts-networking-essentials
type: qa
step: 1
---
## Q
**三层模型与一次请求**｜系统设计 · 核心概念

面试里最常提到网络的哪三层？浏览器打开一个网页时，这三层怎样配合，从中能得到哪三点对系统设计有用的观察？

## A
**要点。** 三层：网络层（Layer 3，IP，负责寻址与路由，尽力而为）、传输层（Layer 4，TCP / UDP / QUIC，提供可靠、有序、流控）、应用层（Layer 7，DNS、HTTP、WebSocket、WebRTC）。

一次请求的顺序：DNS 解析出 IP → TCP 三次握手（SYN、SYN-ACK、ACK）→ 发 HTTP 请求 → 服务端处理 → 返回响应 → 四次挥手（FIN、ACK、FIN、ACK）关闭。

**为什么。** 三点观察：
- 应用可以默认数据可靠有序，不用关心路由与电信号。
- 一个「请求」背后有很多包往返，越往上层延迟和处理越多（所以后面选 L4 还是 L7 负载均衡有代价差异）。
- 连接是双方都要维护的状态；没有 keep-alive 或 HTTP/2 多路复用，每个请求都要重建连接。长连接场景（实时推送）因此要特别设计。

**易错。** 不要在面试里展开握手细节，只需说清上面三点。
