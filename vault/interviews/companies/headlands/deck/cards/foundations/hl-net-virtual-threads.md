---
id: hl-net-virtual-threads
node: foundations.networking-basics
type: qa
step: 37
---
## Q
JDK 21 的虚拟线程（virtual thread，JEP 444）怎么在阻塞式套接字 I/O 上获得接近 NIO 的扩展性？写出每连接一个虚拟线程的服务器骨架。

## A
虚拟线程是 JVM 调度的轻量线程，创建几乎免费，可同时有几十万个，运行在少量**载体线程**（carrier，默认数 = CPU 核数）上。它调用阻塞套接字 I/O（`Socket.read`、`ServerSocket.accept`）时，JDK 内部用非阻塞 I/O + poller（epoll / kqueue）把它**挂起**（unmount，栈存到堆里），**释放载体线程**去跑别的虚拟线程，数据就绪再恢复。程序员写的是普通阻塞代码。

```java
try (var server = new ServerSocket(0);
     var pool = Executors.newVirtualThreadPerTaskExecutor()) {
    while (true) {
        Socket s = server.accept();
        pool.submit(() -> { /* 直白的阻塞 read/write 循环 */ return null; });
    }
}
```
