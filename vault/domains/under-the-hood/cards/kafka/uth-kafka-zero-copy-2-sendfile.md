---
id: uth-kafka-zero-copy-2-sendfile
node: kafka.zero-copy
type: qa
step: 2
---
## Q
**sendfile：数据不经过用户态**｜Kafka · 4.0

consumer 拉取消息时，broker 为什么几乎不花 CPU 搬数据？开了 TLS 之后还是这样吗？

## A
**结构。** 磁盘上的日志格式和网络上的消息批格式相同，fetch 时不用重新编码，直接调 Java 的 `FileChannel.transferTo`，对应 Linux 的 `sendfile`：数据从页缓存直达网卡。

**细节。**

- 传统路径：磁盘 → 页缓存 → 用户缓冲区 → socket 缓冲区 → 网卡，4 次拷贝、2 次系统调用；`sendfile` 只剩最后一次到网卡。
- 多个消费者读同一段数据，它只进页缓存一次。

**坑。** 开了 TLS 就失效：加密要在用户态做，`SslTransportLayer` 只能每次读 32768 字节文件、加密、再写出。

**对应 LeetCode：** 无直接对应的题（系统调用层面的优化）
