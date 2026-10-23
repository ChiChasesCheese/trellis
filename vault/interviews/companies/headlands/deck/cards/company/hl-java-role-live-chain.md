---
id: hl-java-role-live-chain
node: company.java-role
type: qa
step: 2
---
## Q
一笔交易背后的"实盘链路"依次经过哪几个组件？配套有哪些系统？

## A
实盘链路必须极快，依次是：
1. 交易所发出行情；
2. **行情 parser**（market data parser）解析；
3. **strategy** 决定怎么交易；
4. **order gateway** 把订单发出；
5. 回到交易所。

配套系统：**monitoring GUI**（监控界面）、**drop copy**（交易所回传的成交副本，用来对账）、**market data capture**（行情落盘）。

Java 岗大概率不在这条极快链路上，而在下面的"离线 + 配套"那一半。
