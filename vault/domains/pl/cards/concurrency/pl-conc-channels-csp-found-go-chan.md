---
id: pl-conc-channels-csp-found-go-chan
node: concurrency.channels-csp
type: qa
step: 2
---
## Q
Go 的 channel 是什么？无缓冲和有缓冲 channel 在行为上有什么区别，`close` 和 `range` 怎么配合？

## A
**channel**（通道）是 goroutine 之间传递值的管道，类型化：`chan int` 只能传整数。基本操作：`ch <- v` 发送，`v := <-ch` 接收，`close(ch)` 表示“不会再有数据”。

两种创建方式，行为差别很大：
- **无缓冲**（`make(chan int)`，容量 0）：发送和接收必须**同时就绪**才完成。发送方会阻塞，直到有接收方来取，像两个人当面交接。
- **有缓冲**（`make(chan int, 2)`，容量 2）：内部有一个能装 2 个值的队列。队列没满时发送立刻返回，满了才阻塞；队列空时接收才阻塞。

用一个实验看区别：一个生产者发送 4 个数，主 goroutine 睡 50 毫秒后才开始接收，用原子计数器记录“消费者没动时已完成了几次发送”：
```go
ch := make(chan int, c)             // c = 0 or 2
var sent atomic.Int32
go func() {
    for i := 1; i <= 4; i++ { ch <- i; sent.Add(1) }
    close(ch)
}()
time.Sleep(50 * time.Millisecond)
fmt.Printf("cap %d: sends finished before any receive = %d\n", c, sent.Load())
for range ch {}
```
输出：`cap 0: sends finished before any receive = 0`，`cap 2: sends finished before any receive = 2`。容量 0 时第一次发送就卡住；容量 2 时能先放 2 个，第 3 个才卡住。

`close(ch)` 后：已缓冲的数据仍可被取完，之后的接收立即返回零值并带 `ok=false`；`for v := range ch` 会在数据取完且通道关闭时自动结束。这样生产者通过 `close` 告诉消费者“没有更多了”。只有发送方应该关闭通道，向已关闭的通道发送会 panic。
