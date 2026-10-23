---
id: hft-fix-application-layer
node: protocols.fix
type: qa
step: 3
---
## Q
FIX 协议（Financial Information eXchange）的应用层里，一笔订单从提交到成交，来回会交换哪几种主要消息？

## A
应用层负责订单本身的业务含义。主要消息：

| 方向 | 消息 | 类型码 |
|---|---|---|
| 客户 → 交易所/券商 | 新订单 NewOrderSingle | `35=D` |
| 客户 → 交易所/券商 | 撤单请求 OrderCancelRequest | `35=F` |
| 客户 → 交易所/券商 | 改单请求 OrderCancelReplaceRequest | `35=G` |
| 对方 → 客户 | 执行回报 ExecutionReport | `35=8` |

**执行回报**是核心：订单被接受、部分成交、全部成交、被撤、被拒，都用它通知，由其中的订单状态字段（`39=OrdStatus`）和本次成交量（`32=LastQty`）、成交价（`31=LastPx`）区分。

例子：买 100 股，先收到一条"已接受"，再收到一条"成交 40 股"，再一条"成交 60 股，订单完成"。

你必须以回报为准更新自己的持仓，不能假设"发出去了就是成交了"。
