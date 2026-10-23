---
id: hl-net-delayed-ack
node: foundations.networking-basics
type: qa
step: 21
---
## Q
延迟确认（Delayed ACK）是什么？Linux 上等多久？

## A
接收方不是收到每个段都立刻回 ACK，而是**稍等一下**（Linux 最小约 **40 ms**，RFC 1122 允许最多 500 ms），看有没有数据要回（顺便捎带 ACK），或再来一个段（两个段合并确认一次）。目的同样是少发小包。
