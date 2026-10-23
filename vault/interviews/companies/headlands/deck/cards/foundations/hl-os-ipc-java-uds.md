---
id: hl-os-ipc-java-uds
node: foundations.os-processes-threads-ipc
type: qa
step: 18
---
## Q
Java 16+ 怎么使用 Unix 域套接字（Unix domain socket）？其余 IPC 方式在 Java 里怎么做？

## A
JEP 380：
```java
Path sock = Path.of("/tmp/demo.sock");
try (ServerSocketChannel server = ServerSocketChannel.open(StandardProtocolFamily.UNIX)) {
    server.bind(UnixDomainSocketAddress.of(sock));   // 绑定到文件系统路径
}
```
客户端用 `SocketChannel.open(UnixDomainSocketAddress.of(sock))` 连接，API 与 TCP 的 `SocketChannel` 完全相同。

其他：
- **共享内存**：Java 没有直接的 `shm_open`，做法是**映射同一个文件**；Linux 上放 `/dev/shm`（tmpfs）里映射就是纯内存共享，没有磁盘写回；
- **消息队列**：很少用 OS 级的，业界用库：Aeron（UDP / IPC）、Chronicle Queue（映射文件）、Agrona（共享内存数据结构）。
