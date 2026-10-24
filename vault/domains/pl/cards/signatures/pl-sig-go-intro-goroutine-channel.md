---
id: pl-sig-go-intro-goroutine-channel
node: signatures.go
type: qa
step: 2
---
## Q
goroutine 和通道（channel）是什么？Go 的格言“通过通信来共享内存，而不是通过共享内存来通信”在一个流水线例子里是什么意思？

## A
**goroutine**：在函数调用前加 `go`，这个调用就作为一个**轻量的并发执行单元**启动，不阻塞当前代码。它由 Go 运行时调度到少量系统线程上，初始栈约 2 KB，一个程序里开几十万个也没问题。

**通道**（channel）：goroutine 之间传递值的带类型的管道。`ch <- v` 发送，`v := <-ch` 接收。无缓冲通道的发送和接收会**同步**（双方都到达才完成）；带缓冲的在缓冲满时才阻塞。关闭通道表示“不会再有数据”，`for v := range ch` 会在关闭后结束。

**格言的含义**：不要让多个 goroutine 同时读写同一个变量并用锁保护，而是让**数据的所有权随消息转移**——谁收到值，谁就独占它。

```go
nums := make(chan int); sq := make(chan int)
go func() { defer close(nums); for i := 1; i <= 5; i++ { nums <- i } }()
go func() { defer close(sq); for n := range nums { sq <- n * n } }()
for v := range sq { fmt.Print(v, " ") }
```

完整程序（用 `strings.Join` 拼接输出）的真实输出：`1,4,9,16,25`。两个 goroutine 构成一条流水线：第一段产生数字，第二段求平方，主 goroutine 消费，三者之间只通过通道通信，没有任何锁。

**来源**：这是 Tony Hoare 的 CSP（通信顺序进程）模型，Go 把它做进语言的语法和运行时。

**要记住的一点**：goroutine 让“为每个并发任务写一段直线代码”变得廉价，通道让它们之间的协作有清晰的数据流。这是 Go 最有辨识度的特性，也是它在云服务领域胜出的主要原因。
