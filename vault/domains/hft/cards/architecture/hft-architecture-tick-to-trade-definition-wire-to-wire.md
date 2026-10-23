---
id: hft-architecture-tick-to-trade-definition-wire-to-wire
node: architecture.tick-to-trade
type: qa
step: 1
---
## Q
交易系统常说的 tick-to-trade 延迟（也叫 wire-to-wire）是从哪一刻量到哪一刻？为什么要在网线上量，而不是在程序里量？

## A
tick-to-trade 指：一条行情更新（tick）的包**到达网卡**，到由它触发的订单（trade）的包**离开网卡**，中间经过的时间。wire-to-wire 就是"线到线"。

在程序里用 `System.nanoTime()` 打点，只能量到应用拿到数据之后的那一段；网卡接收、DMA 把包拷进内存、内核或旁路驱动里的处理、网卡发送这些时间都量不到。

可靠的做法：用网络分流器（tap）或交换机镜像，把行情进、订单出这两个包都打上**硬件时间戳**，相减得到真实的 wire-to-wire。程序内的打点只用来把总时间拆成各环节。
