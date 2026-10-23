---
id: hft-sbe-mdp3-channels
node: protocols.sbe-mdp3
type: qa
step: 3
---
## Q
CME 的行情协议 MDP 3.0（Market Data Platform 3.0）是怎么组织的？它用了哪些通道，一个数据包里有什么？

## A
MDP 3.0 是 CME 期货和期权的行情协议，消息用 SBE 编码，通过 UDP 组播发送，和 Nasdaq 的 ITCH 思路相近。

**通道（channel）：**
- **增量刷新通道**（incremental refresh）：实时的订单簿变化，A、B 两条线冗余发送。
- **快照通道**（snapshot recovery）：循环广播各品种的完整订单簿，供中途加入或大缺口时恢复用。
- **合约定义通道**（instrument definition）：每个合约的规格，如代码、最小变动价位、到期日。

**数据包结构：**
- 包头 12 字节：4 字节的包序号 + 8 字节的发送时间（纳秒）。
- 后面是若干条消息，每条先有 2 字节的长度，再是 SBE 消息头和消息体。

接收方靠包序号发现缺口；一个包里可能含多个品种的更新。

和 ITCH 的区别：ITCH 的序号按消息编，且每条消息是一笔订单的变化；MDP 3.0 的序号按包编，增量消息主要是**按价位聚合**的更新（某价位现在多少股、多少笔订单）。
