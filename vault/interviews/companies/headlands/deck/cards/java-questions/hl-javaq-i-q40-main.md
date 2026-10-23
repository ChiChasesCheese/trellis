---
id: hl-javaq-i-q40-main
node: java-questions.i-network
type: qa
step: 1
---
## Q
讲一讲与延迟相关的 TCP 基础：握手、Nagle 算法、延迟 ACK、`TCP_NODELAY`。
Explain TCP basics relevant to latency: handshake, Nagle's algorithm, delayed ACK, `TCP_NODELAY`.

## A
一句话：TCP 是可靠的字节流（三次握手建连、序号 + 确认、重传、拥塞控制）。**Nagle** 为减少小包，会把小写入攒着等前一个包的 ACK；**延迟 ACK** 让接收方等一会儿再确认；两者叠加会让"写-写-读"模式卡几十毫秒。低延迟程序设置 `TCP_NODELAY`，并把一条消息合成一次写入。

- **握手**：C → S：SYN；S → C：SYN+ACK；C → S：ACK。1 个 RTT 后才能发数据；长连接复用避免这个成本。
- **Nagle**：有未确认数据时，小于 MSS 的新数据先缓存，等 ACK 或凑满再发。
- **延迟 ACK**：接收方收到数据不立刻 ACK，等最多约 40 ms（Linux 常见），看有没有数据可以捎带。
