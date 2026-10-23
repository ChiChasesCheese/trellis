---
id: hft-moldudp64-gap-detection
node: protocols.moldudp64
type: qa
step: 2
---
## Q
MoldUDP64 的接收方是怎么用序号判断丢包、重复和乱序的？请用一个数字例子说明。

## A
接收方始终记着"下一条期望的序号"（expected），每收到一个包就和头里的 Sequence Number 比较：

- **相等：** 正常，处理这个包里的消息，expected += Message Count。
- **大于 expected：** 有缺口（gap），中间的消息丢了或还在路上。
- **小于 expected：** 这个包已经处理过，是重复包（比如另一条冗余线路的副本），丢弃。

例子：expected = 1000，收到一个包 Sequence = 1005、Count = 3。
- 1005 > 1000，说明 1000 到 1004 这 5 条消息缺失。
- 这个包里的 1005 到 1007 先不处理（订单簿要按顺序更新），或缓存起来，同时向重传服务器请求 1000 到 1004。
- 补齐后，再处理 1005 到 1007，expected 变为 1008。

这样接收方不需要 TCP 的"一律等"机制，而是自己决定如何补救。
