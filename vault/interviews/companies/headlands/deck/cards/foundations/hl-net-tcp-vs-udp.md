---
id: hl-net-tcp-vs-udp
node: foundations.networking-basics
type: qa
step: 14
---
## Q
TCP 与 UDP 在连接、可靠性、传输单位、头部、延迟、一对多、适用场景上怎么对比？

## A
- 连接：TCP 面向连接（握手）；UDP 无连接。
- 可靠性：TCP 可靠有序；UDP 尽力而为，可能丢、乱、重。
- 单位：TCP 是字节流（无边界）；UDP 是数据报（有边界）。
- 头部：TCP ≥ 20 B；UDP 8 B。
- 延迟：TCP 受重传、队头阻塞、Nagle 影响；UDP 最小，无额外机制。
- 一对多：TCP 不支持；UDP **支持组播 / 广播**。
- 适用：TCP 用于订单、文件、HTTP；UDP 用于行情、DNS、音视频、游戏。
