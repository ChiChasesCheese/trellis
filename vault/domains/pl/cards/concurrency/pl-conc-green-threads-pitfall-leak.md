---
id: pl-conc-green-threads-pitfall-leak
node: concurrency.green-threads
type: qa
step: 9
---
## Q
Go 里调用 1000 次一个「起 goroutine 往无缓冲 channel 发数据、自己提前返回」的函数，会留下多少个 goroutine？为什么便宜的 goroutine 反而更容易泄漏？

## A
会永久留下 1000 个。代码：
```go
func fetch() int {
    ch := make(chan int) // unbuffered
    go func() { ch <- 42 }()
    return 0 // returns early, nobody receives
}

for i := 0; i < 1000; i++ { fetch() }
fmt.Println("goroutines:", runtime.NumGoroutine())
```
输出：`goroutines: 1001`（1000 个泄漏的加上 main）。

原因：无缓冲 channel 的发送要等有人接收。`fetch` 返回后没有任何代码会接收，这个 goroutine 永远阻塞在 `ch <- 42`；运行时只会回收「已经结束」的 goroutine，不会回收「永远等不到」的 goroutine，GC 也不会，因为它仍被 channel 等待队列引用着。

为什么便宜反而危险：创建几乎没有成本，也没有句柄可以追踪（`go f()` 不返回任何对象），泄漏的 goroutine 平时没有症状，只是内存和 goroutine 数缓慢上涨，直到进程 OOM。

对策：
- 给 channel 留足缓冲（这里 `make(chan int, 1)` 就能让发送立即完成并让 goroutine 退出）。
- 用 `context.Context` 取消并在 `select` 里监听 `ctx.Done()`。
- 监控 `runtime.NumGoroutine()`，测试里检查泄漏。