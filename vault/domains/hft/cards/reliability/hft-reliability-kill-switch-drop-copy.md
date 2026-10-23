---
id: hft-reliability-kill-switch-drop-copy
node: reliability.kill-switch
type: qa
step: 3
---
## Q
drop copy 是什么？为什么用它做独立核对，比只信自己订单网关收到的回报更可靠？

## A
drop copy 是交易所通过**另一条独立的会话**，把我们账户的所有订单回报和成交的副本发给另一个接收方，比如独立的风控或对账系统。

主交易会话的回报走我们自己的订单网关，drop copy 不经过它。价值在于**独立性**：如果网关有 bug，漏掉或错解了一条成交回报，内部持仓就会错；而 drop copy 的接收方是另一套代码，它独立算出的持仓和内部不一致，就能立刻发现差异（break）并触发出错即停。

例：网关漏掉了一笔 500 股的成交，内部持仓显示 0，drop copy 侧算出 500，对比之后立刻告警。
