---
id: pl-foundations-lineage-found-go-goroutine-channel
node: foundations.lineage
type: qa
step: 2
---
## Q
Go 的 goroutine 和 channel 是什么？它们描述的并发模型（CSP）核心思想是什么？

## A
goroutine 是 Go 运行时调度的轻量级执行单元：在函数调用前加 `go` 关键字，这个函数就和调用者并发地运行。它不是操作系统线程，初始栈只有几 KB，可以同时存在几十万个，由运行时把它们分配到少量系统线程上。

channel（通道）是类型化的管道，用来在 goroutine 之间传递值：`ch <- v` 发送，`<-ch` 接收。无缓冲的通道让发送者和接收者「碰头」，一方先到就阻塞等待另一方，所以通道同时起到传递数据和同步的作用。

```go
ch := make(chan string)
go func() { ch <- "ping" }()   // 另一个 goroutine 发送
fmt.Println(<-ch)              // 主 goroutine 接收，输出 ping
```

实际输出 `ping`。主 goroutine 在接收处阻塞，直到另一个 goroutine 发来消息。

背后的思想是 CSP（Communicating Sequential Processes，1978 年 Tony Hoare 提出）：独立的顺序进程，不共享状态，只通过消息通信。Go 的口号是「不要通过共享内存来通信，而要通过通信来共享内存」：数据的所有权随消息转移，同一时刻只有一个 goroutine 持有它，从而不需要锁。
