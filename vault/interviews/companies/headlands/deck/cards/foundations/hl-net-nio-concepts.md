---
id: hl-net-nio-concepts
node: foundations.networking-basics
type: qa
step: 32
---
## Q
NIO 的非阻塞模式、`SelectionKey` 和 `interestOps` 各是什么？为什么「可读」不等于「消息完整」？

## A
- **非阻塞模式** `configureBlocking(false)`：`read` 没数据立即返回 0，`write` 缓冲区满就写一部分（或 0）；
- **SelectionKey**：通道在 selector 上的注册；`interestOps` 是关心的事件：`OP_ACCEPT`、`OP_READ`、`OP_WRITE`、`OP_CONNECT`。
- **就绪不等于完成**：可读只表示「此刻读不会阻塞」，不表示一个完整消息到了，因为 TCP 是字节流。
