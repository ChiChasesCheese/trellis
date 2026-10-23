---
id: hl-net-socket-api
node: foundations.networking-basics
type: qa
step: 4
---
## Q
套接字（socket）是什么？TCP 服务端和客户端的标准调用顺序是什么？Java 里对应哪些类？

## A
套接字是 OS 提供给应用程序的网络通信接口，在 Unix / Linux 里也是一个**文件描述符**（整数），可以 `read` / `write` / `close`。

服务端：`socket()` 创建 → `bind()` 绑定（IP, 端口）→ `listen()` 开始监听并设等待队列（backlog）→ `accept()` 阻塞等待连接。客户端：`socket()` → `connect()` 发起连接 → 三次握手完成 → 双方 `read()` / `write()` → 各自 `close()`。这套 Berkeley sockets API 自 1983 年没变。

Java 对应：`ServerSocket` / `Socket`（阻塞）；`ServerSocketChannel` / `SocketChannel`（NIO）。
