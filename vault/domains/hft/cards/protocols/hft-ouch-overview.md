---
id: hft-ouch-overview
node: protocols.ouch
type: qa
step: 1
---
## Q
Nasdaq 的 OUCH 协议是做什么的？它包含哪些主要的消息？

## A
OUCH 是 Nasdaq 的**二进制下单协议**（行情用 ITCH，下单用 OUCH）。它跑在一条 TCP 连接上，登录和心跳由 SoupBinTCP 会话协议处理。

**客户端发给交易所：**
- Enter Order（`O`）：下新单，带股票、方向、股数、价格、有效期等。
- Replace Order（`U`）：改单，给一个新的订单标识、股数、价格。
- Cancel Order（`X`）：撤单（也可以把股数降低）。

**交易所回报：**
- Accepted（`A`）：订单被接受，进入订单簿。
- Executed（`E`）：订单被（部分）成交，带成交股数和价格。
- Canceled（`C`）：订单被撤销，带原因（比如用户请求撤销，或立即成交否则取消，即 IOC，订单没成交的部分被取消）。
- Rejected（`J`）：订单被拒绝。

**怎么跟踪订单：** 每个订单由客户自己指定一个唯一的**订单标识**（OUCH 4.2 里叫 order token，是个 14 字符的字段），回报都带着它，你据此对应到自己的订单。
