---
id: hi-sd-networking-essentials-2-tcp-udp
node: qb.sd.messenger-chat-system.pre-sd-core-concepts-networking-essentials
type: qa
step: 2
---
## Q
**TCP 与 UDP**｜系统设计 · 核心概念

设计里默认用 TCP，什么时候该改用 UDP？UDP 在浏览器端有什么限制，常见的折中是什么？

## A
**要点。** TCP 面向连接，保证送达、保序，带流控与拥塞控制，头部 20–60 字节。UDP 无连接，只负责带上源和目的 IP、端口，不保证送达和顺序，头部仅 8 字节，延迟更低。

**取舍。** 面试默认 TCP，几乎不用特意提。只有同时满足下面情形才值得选 UDP：延迟比完整性更重要（游戏、语音、直播）、可容忍少量丢包（视频流、高频遥测）、客户端不是浏览器。丢包时直接丢掉一小段音频，比重传并占满网络更划算。

**易错。** 浏览器除 WebRTC 外基本不支持 UDP。比如直播评论区的点赞和表情刷屏：App 端可走 UDP 实时流，浏览器端退回批量的 HTTP，在界面上摊开播放。

**补充。** QUIC 可看成「更现代的 TCP」，但普及度还不够，只当加分项。
