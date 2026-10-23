---
id: hft-itch-messages-overview
node: protocols.itch-messages
type: qa
step: 1
---
## Q
Nasdaq ITCH 5.0 行情协议里，重建订单簿用到的主要消息有哪些？每种对订单簿有什么影响？

## A
每条消息的第 1 个字节是类型字母。主要的几种：

| 类型 | 消息 | 对订单簿的影响 |
|---|---|---|
| `A` | Add Order 新增订单 | 在某价位队尾加一笔订单 |
| `E` | Order Executed 订单成交 | 订单被（部分）吃掉，数量减少 |
| `X` | Order Cancel 部分撤单 | 订单数量减少，订单仍在 |
| `D` | Order Delete 删除订单 | 整笔订单消失 |
| `U` | Order Replace 替换订单 | 删掉旧订单，加一笔新的（新编号、新价格或数量） |
| `P` | Trade 成交 | 不可见订单的成交，**不改订单簿**，只是成交记录 |
| `S` | System Event 系统事件 | 开盘、收盘等，用来知道一天的阶段 |

注意：只有 `A`、`E`、`X`、`D`、`U` 会改订单簿。`P` 对应的是隐藏订单（hidden order，不在订单簿上显示），所以簿上看不到它，只能在成交记录里看到。
