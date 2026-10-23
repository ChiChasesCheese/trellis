---
id: hl-net-multicast-mechanics
node: foundations.networking-basics
type: qa
step: 26
---
## Q
组播的组地址范围、IGMP、IGMP snooping、TTL 各是什么？组播用 TCP 还是 UDP？

## A
- **组地址**：IPv4 的 `224.0.0.0/4`（224.x.x.x – 239.x.x.x）；`239.0.0.0/8` 是「本地管理」范围，私有网络里随便用。
- **加入组**：接收方用 **IGMP** 告诉本地交换机或路由器「我想收这个组」；交换机用 **IGMP snooping** 只把该组流量转发到有订阅者的端口。
- **TTL**：控制组播包能跨几跳路由器，TTL = 1 表示只在本网段。
- 组播只能用 **UDP**。
