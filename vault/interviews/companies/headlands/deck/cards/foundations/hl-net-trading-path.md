---
id: hl-net-trading-path
node: foundations.networking-basics
type: qa
step: 1
---
## Q
交易系统一条链路的网络部分大致怎么走？面试常围绕网络问哪几类问题？

## A
链路：交易所 →（UDP 组播行情）→ 行情解码 → 策略 → 风控 → 订单网关 →（TCP 或专有协议）→ 交易所。整条回路往返延迟是**微秒级**，每一微秒都有人在量。

面试常问：
- TCP 和 UDP 的区别？
- 为什么交易所行情用组播？
- Nagle 算法是什么，为什么设 `TCP_NODELAY`？
- 延迟和吞吐的区别？
- 什么叫内核旁路（kernel bypass）？
- Java 里怎么写网络程序，NIO 和虚拟线程怎么选？
