---
id: pl-conc-ioruntimes-found-java
node: concurrency.io-runtimes
type: qa
step: 3
---
## Q
Java 的 NIO `Selector` 是什么？JDK 21 起虚拟线程里的阻塞 `socket.read()` 又是怎样做到不占平台线程的？

## A
**NIO `Selector`**（Java 1.4 引入）是 Java 对 `epoll`/`kqueue` 的包装：把非阻塞的 `Channel` 注册到 `Selector`，声明关心的事件（`OP_ACCEPT`、`OP_READ`……），然后一个线程调用 `select()` 睡眠，被唤醒时遍历就绪的 key 并处理。实测，3 个客户端、1 个线程：
```java
sel.select();                                 // sleep until some channel is ready
for (SelectionKey k : sel.selectedKeys()) {
    if (k.isAcceptable()) { /* accept, register OP_READ */ }
    else if (k.isReadable()) { /* read from k.channel() */ }
}
```
输出：`main read hi2`、`main read hi1`、`main read hi0`：三条连接由同一个线程 `main` 按**就绪顺序**处理（最晚启动的客户端等待最短，所以最先到）。业界的 Netty 就是在这个基础上做的事件驱动框架，代价是编程模型是回调和状态机。

**虚拟线程如何借用这套机制**：虚拟线程里调用普通的阻塞 `InputStream.read()`，JDK 内部：
1. 以非阻塞方式尝试读；
2. 读不到数据就**挂起这个虚拟线程**（它的栈被保存到堆上，载体线程转去跑别的虚拟线程）；
3. 把这个 fd 登记给 JDK 内部的轮询线程（线程名 `Read-Poller` 和 `Write-Poller`，里面是 `epoll`/`kqueue`）；
4. 事件到来，轮询线程把虚拟线程重新放回调度队列。

用 `jcmd <pid> Thread.print` 看一个有 200 个连接的服务（每个连接一个虚拟线程），平台线程只有约三十个：JVM 自身的线程，十几个 `ForkJoinPool-1-worker-N` 载体线程，以及 `Read-Poller`、`Write-Poller`。实测 5000 个空闲连接时线程数 21 到 35，内存从 43 MB 到 73 MB，平均每连接约 6 KB。

**设计后果**：这是同一个 `java.io` 的 API，不需要改写成回调；但**只有 JDK 改造过的阻塞点**才会挂起虚拟线程（网络 I/O、`sleep`、`java.util.concurrent` 锁等）。仍然会钉住载体线程的情形（比如在原生方法里阻塞）需要排查，普通文件 I/O 则是由运行时临时补充载体线程来补偿。
