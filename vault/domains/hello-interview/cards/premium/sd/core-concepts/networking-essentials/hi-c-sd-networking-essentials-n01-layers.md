---
id: hi-c-sd-networking-essentials-n01-layers
node: sd.core-concepts.networking-essentials.notes
type: qa
step: 1
---
## Q
**网络基础 · 网络分层与三个关键层**｜摘要 · 必会

为什么网络要分层？设计面试里最常用到哪三层，各管什么？

## A
- **分层的意义：** 网络按层次抽象（所谓 OSI 模型），让应用开发者只需关心相邻的下一层。就像你用语言里的 `open` 读文件，而不是手动指挥磁盘怎么读字节；请求网页时也不用知道电线上什么电压代表 0 和 1。
- **网络层（Layer 3，IP）：** 负责寻址和路由，把数据拆成包、在网络之间转发，尽力而为地送到任意目的 IP。同层还有 InfiniBand（大规模机器学习训练用），但面试里基本就是 IP。
- **传输层**（Layer 4，TCP / UDP / QUIC）： 在网络层之上提供端到端通信服务，如可靠性、有序、流量控制。
- **应用层**（Layer 7，DNS、HTTP、WebSocket、WebRTC）： 构建在 TCP（WebRTC 是 UDP）之上，为 Web 应用常见的数据类型提供抽象。
- **面试强度：** 网络在基础设施和分布式系统岗位更受重视，全栈或产品岗位了解表层即可；但面试官可能刚值完负载均衡或 CDN 的班，要有备而来。
