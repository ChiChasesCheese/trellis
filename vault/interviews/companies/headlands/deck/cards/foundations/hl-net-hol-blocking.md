---
id: hl-net-hol-blocking
node: foundations.networking-basics
type: qa
step: 10
---
## Q
什么是 TCP 的队头阻塞（head-of-line blocking）？它与交易所行情用 UDP 组播有什么关系？

## A
TCP 保证有序，所以第 2 段丢了，第 3、4、5 段即使已经到了，**应用也读不到**，它们在内核缓冲区里等第 2 段重传。一次丢包让后面所有数据延迟一个 RTT 甚至一个 RTO。

这是交易所行情**用 UDP 组播而不用 TCP** 的重要原因：行情里旧消息丢了，与其等它不如先处理新的，缺的另补。
