---
id: hl-net-nodelay-fixes
node: foundations.networking-basics
type: qa
step: 23
---
## Q
解决 Nagle 与延迟确认停顿有哪三种办法？在 Java 里怎样设置 `TCP_NODELAY`？

## A
1. **`TCP_NODELAY`**：关闭 Nagle，写下去立刻发。低延迟交易系统几乎总是设置它。
2. **一次写完**：header 和 body 拼进同一个缓冲区一次 `write`，或聚集写（`GatheringByteChannel.write(ByteBuffer[])` / `writev`），更根本，避免产生「写-写-读」模式。
3. `TCP_QUICKACK`（Linux）：关闭延迟确认，但每次 `read` 后要重新设置。

```java
s.setTcpNoDelay(true);                                          // Socket
ch.setOption(StandardSocketOptions.TCP_NODELAY, true);          // SocketChannel
ch.setOption(StandardSocketOptions.SO_RCVBUF, 1 << 20);         // 接收缓冲区 1 MB
```
