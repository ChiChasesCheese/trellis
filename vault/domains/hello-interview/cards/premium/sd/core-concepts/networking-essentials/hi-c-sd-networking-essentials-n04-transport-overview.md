---
id: hi-c-sd-networking-essentials-n04-transport-overview
node: sd.core-concepts.networking-essentials.notes
type: qa
step: 4
---
## Q
**网络基础 · 传输层：TCP、UDP、QUIC**｜摘要 · 必会

传输层提供什么？三个协议里面试到底要在哪两个之间选？

## A
- **作用：** 在应用之间建立端到端通信，给出一些保证，而不是丢给你一堆杂乱的包。
- **三个协议：** TCP、UDP、QUIC。多数面试里真正的选择只在 TCP 和 UDP 之间。
- **QUIC：** 新协议，想在保留 TCP 优点的同时做现代化和性能改进。越来越流行，但还不普及，面试里可以把它当作"更好但采用度不如 TCP 的 TCP"。
- **分寸：** 追求性能的面试官可能会欣赏你懂 QUIC 和 HTTP/3，但多数系统设计面试官希望你把时间花在设计的其他部分。
