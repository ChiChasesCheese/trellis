---
id: pl-conc-channels-csp-pitfall-deadlock
node: concurrency.channels-csp
type: qa
step: 11
---
## Q
Go 里对没人接收的无缓冲 channel 发送，或者往已关闭的 channel 发送，分别会发生什么？还有哪些常见的通道陷阱？

## A
1. **没人接收的发送 → 死锁**：
```go
ch := make(chan int)
ch <- 1
```
输出：`fatal error: all goroutines are asleep - deadlock!`，随后是 `goroutine 1 [chan send]:`，程序退出码 2。运行时发现所有 goroutine 都阻塞了、不可能再被唤醒，于是直接终止。注意：只有当**全部** goroutine 都卡死时才会报告；只要程序里还有别的 goroutine 在运行（比如一个 HTTP 服务器），部分 goroutine 的死锁是静悄悄的，表现为泄漏。

2. **向已关闭的通道发送 → panic**：
```go
ch := make(chan int, 1)
close(ch)
ch <- 1
```
输出：`panic: send on closed channel`。关闭已关闭的通道也会 panic。规则：只由**发送方**关闭，接收方永远不关闭；有多个发送方时要用额外的同步（如 `sync.WaitGroup` 等所有发送方结束后再关）。

3. **从已关闭的通道接收**不会阻塞，而是立刻返回零值和 `ok=false`，所以要用 `v, ok := <-ch` 或 `for range` 区分「读到 0」和「通道已结束」。

4. **对 `nil` 通道收发会永远阻塞**，常被故意用在 `select` 里关掉某个分支。

5. **无界队列堆积**：Rust 的 `mpsc::channel()`、Python 的 `Queue()` 默认无界，生产快于消费时内存会无限增长，没有背压。生产系统里应该使用有界容量。
