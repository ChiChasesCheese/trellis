---
id: pl-conc-iomodels-mechanism-drain
node: concurrency.io-models
type: qa
step: 5
---
## Q
事件循环收到“某连接可读”后，应该怎样读？电平触发（level-triggered）和边沿触发（edge-triggered）的区别是什么，为什么要“读到 EAGAIN 为止”？

## A
一次就绪事件之后，缓冲区里可能积了很多数据，而你每次 `recv` 只取一部分。事件循环处理一个连接的标准流程：

1. 内核通知该 fd 可读；
2. 循环 `recv`，直到取完；
3. 回到 `epoll_wait`/`kqueue` 等下一个事件。

实测：往一个非阻塞套接字写入 5000 字节，每次最多读 1024：
```python
while True:
    try: d = a.recv(1024)
    except BlockingIOError: break    # EAGAIN: drained
    reads += 1; got += len(d)
```
输出 `reads: 5 bytes: 5000 -> then EAGAIN`：读了 5 次，第 6 次返回 `EAGAIN`，说明已排空。

**两种通知语义**：
- **电平触发**（`select`、`poll`、默认的 `epoll`；`kqueue` 默认也是）：只要缓冲区里还有数据，每次询问都报告“可读”。简单、安全：这次没读完，下一轮还会提醒你。
- **边沿触发**（`epoll` 的 `EPOLLET`）：只在状态**变化**的那一刻报告一次（从“空”到“非空”）。如果这次只读了一部分就返回，剩下的数据**不会再触发通知**，连接就“卡住”了。所以边沿触发要求每次必须读到 `EAGAIN`。

好处是边沿触发减少了重复唤醒，吞吐更高；代价是更容易写出“偶尔丢事件”的 bug。

**还要考虑公平性**：一个连接数据特别多，读到 `EAGAIN` 会霸占事件循环；成熟的实现会限制单个连接每轮最多读多少，让其他连接先跑。

这也是为什么 Go、tokio 这些运行时把这件事做在内部：用户代码调用 `conn.Read` 或 `.await`，运行时负责“读到 `EAGAIN` 就挂起当前任务，等下一次就绪”。
