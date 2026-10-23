---
id: hl-net-qa-nagle
node: foundations.networking-basics
type: qa
step: 43
---
## Q
面试题：什么是 Nagle？为什么要 `TCP_NODELAY`？

## A
推荐答法：
- Nagle 把小写入攒起来，直到前面数据被确认或攒满一个 MSS，减少小包；
- 它和接收方的延迟确认（Linux 约 40 ms）叠加，在**写-写-读**模式下每个请求多 40 ms；
- 交易系统发订单是延迟敏感的小消息，所以设 `TCP_NODELAY`；更根本的做法是**一次写完整个消息**，避免写-写-读；
- Nagle 的本意：20 万次 1 字节写，开着 Nagle 反而快 4–5 倍。
