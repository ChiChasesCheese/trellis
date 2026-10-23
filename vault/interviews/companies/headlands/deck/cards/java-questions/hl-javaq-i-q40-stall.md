---
id: hl-javaq-i-q40-stall
node: java-questions.i-network
type: qa
step: 2
---
## Q
Nagle 算法和延迟 ACK 叠加为什么会让"写 header 再写 body"卡约 40 ms？在 Java 里怎么修？

## A
- 发送方 `write(header 4B); write(body 4B)`：第二个小包被 **Nagle** 扣住，等 header 的 ACK。
- 接收方要等第二块数据才处理 / 回包，不回数据，**延迟 ACK** 等到超时才确认——约 40 ms 的卡顿（Linux 上的常见现象）。
- Java 修法：`socket.setTcpNoDelay(true)`，NIO 用 `StandardSocketOptions.TCP_NODELAY`。
- **更好的做法**：一次 `write` 发完整条消息（或 gather write），不依赖关掉 Nagle。
