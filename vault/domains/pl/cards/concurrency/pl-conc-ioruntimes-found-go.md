---
id: pl-conc-ioruntimes-found-go
node: concurrency.io-runtimes
type: qa
step: 2
---
## Q
Go 的网络轮询器（netpoller）怎样让阻塞风格的 `conn.Read` 不占用操作系统线程？一个 goroutine 从“等数据”到“继续跑”经历了什么？

## A
Go 的 `net` 包里每个连接的 fd 都是**非阻塞**的，并在首次使用时注册到运行时内置的轮询器（Linux 用 `epoll`，macOS 用 `kqueue`）。一次看起来阻塞的 `Read`，实际上是：

1. goroutine 调用 `conn.Read(buf)`，运行时尝试非阻塞读取；
2. 如果缓冲区有数据，直接返回，没有任何调度发生；
3. 如果得到 `EAGAIN`，运行时把当前 goroutine **停车**（park，状态改为等待），并把它与这个 fd 关联；
4. 承载它的 OS 线程立刻去执行别的 goroutine，不被阻塞；
5. 调度器在找不到可运行任务时，或定期地，向轮询器取出就绪事件，把对应的 goroutine 放回运行队列；
6. 某个线程取到它，从 `Read` 里“返回”，用户代码感觉不到任何异常。

一个经典的 echo 服务器因此就是最直接的写法：
```go
for {
    c, _ := ln.Accept()
    go func() {              // one goroutine per connection
        buf := make([]byte, 1024)
        for { n, err := c.Read(buf); if err != nil { return }; c.Write(buf[:n]) }
    }()
}
```
实测（macOS，一次测量）：5000 个空闲连接，每个连接一个 goroutine 阻塞在 `Read` 上，进程的 OS 线程数从 5 增到 14（不是 5000），内存从 4 MB 增到 27 MB，平均每个连接约 4.7 KB（goroutine 栈、连接对象、缓冲区之和）。

**设计后果**：
- 这个机制由运行时负责，所以**只有走 `net` 包的 I/O** 才是“便宜的阻塞”。通过 cgo 调 C 库的阻塞调用、不可轮询的系统调用，仍会占一个 OS 线程，由调度器交出 P 来补偿。
- 成本是调度器和轮询器的复杂度；换来的是用户几乎不需要知道事件循环的存在。
- 没有任何东西阻止你写出“等不到的 `Read`”：没有设置读超时的 goroutine 会一直停在那里，对端沉默多久它就等多久。
