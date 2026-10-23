---
id: hft-itch-messages-add-order
node: protocols.itch-messages
type: qa
step: 2
---
## Q
ITCH 5.0 的新增订单消息（Add Order，类型 `A`）一共有多少字节？每个字段是什么？

## A
总共 **36 字节**，所有字段定长，按固定偏移排列：

| 字段 | 字节数 | 含义 |
|---|---|---|
| 消息类型 | 1 | 固定为字母 `A` |
| Stock Locate | 2 | 股票的编号 |
| Tracking Number | 2 | Nasdaq 内部跟踪用 |
| Timestamp | 6 | 自午夜起的纳秒数 |
| Order Reference Number | 8 | 订单的唯一编号 |
| Buy/Sell | 1 | `B` 买，`S` 卖 |
| Shares | 4 | 股数 |
| Stock | 8 | 股票代码，右侧补空格 |
| Price | 4 | 价格，4 位小数的整数 |

1+2+2+6+8+1+4+8+4 = 36。

例子：价格字段是 1,502,500，就表示 $150.25；股数字段是 100，就是 100 股。

后续的成交、撤单消息只引用 Order Reference Number，不再重复价格和方向，所以接收方必须自己把这笔订单的信息存下来。
