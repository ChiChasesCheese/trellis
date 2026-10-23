---
id: hl-net-nagle-delayed-ack-stall
node: foundations.networking-basics
type: qa
step: 22
---
## Q
解释 Nagle 与延迟确认叠加造成的「写-写-读」40 ms 停顿：每一步发生了什么？

## A
1. 应用 `write(header 4B)`：无未确认数据，立即发出；
2. 应用 `write(body 40B)`：有未确认数据（header）且小于 MSS，Nagle 把它扣住，等 header 的 ACK；
3. 应用 `read(...)` 等对方回复；
4. 服务端收到 header，但还在等 body 才能处理；延迟确认先不回 ACK，等约 40 ms 看有没有数据可捎带；
5. 客户端的 Nagle 在等 ACK，服务端的延迟确认在等数据或计时器，**互相等**，直到服务端计时器到期。

结果：每个请求 / 响应多出约 **40 ms**（Linux），对交易系统是灾难。
