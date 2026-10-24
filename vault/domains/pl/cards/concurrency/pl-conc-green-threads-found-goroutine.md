---
id: pl-conc-green-threads-found-goroutine
node: concurrency.green-threads
type: qa
step: 2
---
## Q
Go 的 goroutine 是什么？`go` 语句、`sync.WaitGroup` 的基本行为是怎样的，它和线程在使用上有什么不同？

## A
**goroutine** 是 Go 运行时管理的轻量级任务。在任何函数调用前加 `go` 关键字，这次调用就变成一个新的 goroutine，与当前代码**并发**执行，`go` 语句本身立刻返回，不等待。

心智模型：像给后厨递一张新订单——你递完单继续接待下一位客人，不会站着等菜做好。同一个程序里可以同时有几十万个这样的订单，由 Go 运行时分配给少量系统线程去处理。

问题是：`main` 函数一返回，整个程序就结束，不管还有没有 goroutine 在跑。所以需要一种“等它们做完”的办法，最常用的是 `sync.WaitGroup`：先登记要等几个任务，每个任务完成时销一个，`Wait()` 阻塞到全部销完。
```go
var wg sync.WaitGroup
results := make([]int, 3)
for i := 0; i < 3; i++ {
    wg.Go(func() { results[i] = (i + 1) * (i + 1) }) // start a goroutine
}
wg.Wait() // block until all three have finished
fmt.Println(results)
```
输出：`[1 4 9]`。`wg.Go(f)` 是“登记 + 启动 goroutine + 完成时销账”的简写（Go 1.25 起可用）。

和线程相比，使用上的区别：
1. 创建几乎免费（约 0.3 微秒、栈约 2 KB），可以放心为每个任务开一个；
2. 没有返回值，也没有句柄：`go f()` 不会给你可以 `join` 或杀掉它的对象，结果要靠共享变量或 channel 传出，生命周期要靠 `WaitGroup` 或 `context` 管；
3. 切换由 Go 运行时在用户态完成，不是操作系统。
