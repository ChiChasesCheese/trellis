---
id: hl-javaq-i-q41-vt-epoll
node: java-questions.i-network
type: qa
step: 7
---
## Q
虚拟线程做网络 I/O 的吞吐和延迟与手写反应器比怎么样？水平触发和边缘触发 epoll 有什么区别？`io_uring` 在 JDK 21 里怎么样？
What's the difference between level-triggered and edge-triggered epoll?

## A
- **虚拟线程**：写阻塞风格的 `socket.getInputStream().read()`，JDK 在底层转成非阻塞 + poller，吞吐接近反应器，代码像线程模型；但热路径延迟仍不如手写反应器 + 绑核。
- **水平触发**：只要可读就持续通知；**边缘触发**：只在状态变化时通知一次，必须读到 `EAGAIN`。Java `Selector` 用水平触发。
- **`io_uring`**（Linux 的新异步 I/O 接口）：JDK 21 没有官方支持，了解名字即可。
- 最低延迟场景：手写单线程事件循环，绑核，用直接缓冲区，因为没有东西会阻塞它或抢占它。
