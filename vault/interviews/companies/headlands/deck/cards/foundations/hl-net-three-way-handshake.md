---
id: hl-net-three-way-handshake
node: foundations.networking-basics
type: qa
step: 7
---
## Q
TCP 三次握手每一步发什么？它对交易网关的连接策略有什么影响？

## A
1. 客户端发 `SYN (seq=x)`：我想连你，起始序号是 x；
2. 服务端回 `SYN+ACK (seq=y, ack=x+1)`：好，我的起始序号是 y，已收到你的 x；
3. 客户端回 `ACK (ack=y+1)`：收到，连接建立。

握手要 **1 个往返时间（RTT）**才能开始发数据，所以交易网关**长期保持连接**，不为每个订单新建连接。
