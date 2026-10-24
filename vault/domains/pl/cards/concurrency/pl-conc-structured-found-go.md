---
id: pl-conc-structured-found-go
node: concurrency.structured-concurrency
type: qa
step: 2
---
## Q
Go 的 `context.Context` 和 `errgroup` 是什么？它们怎样合起来实现“一个失败，全体取消”？

## A
**`context.Context`** 是 Go 里传递**取消信号和截止时间**的标准方式。它被当作函数的第一个参数一层层传下去。核心方法：
- `ctx.Done()`：返回一个通道，上游取消或超时时这个通道被关闭；
- `ctx.Err()`：取消的原因（`context.Canceled`、`context.DeadlineExceeded`）。
下游在每个阻塞点用 `select` 同时等“自己的工作”和 `<-ctx.Done()`，上游一取消，就立刻放弃。

**`errgroup`**（`golang.org/x/sync/errgroup`，不在标准库）是“一组 goroutine 的作用域”：`g.Go(func() error {...})` 启动子任务；`g.Wait()` 等全部结束，返回**第一个**非 nil 的错误。`errgroup.WithContext(ctx)` 额外返回一个派生的 `ctx`，**第一个子任务出错时这个 ctx 自动被取消**，其余子任务通过它得知该退出。

一个实验：A、C 各需 500 毫秒，B 在 100 毫秒后失败：
```go
g, ctx := errgroup.WithContext(context.Background())
g.Go(func() error { return work(ctx, "A", 500*time.Millisecond, false) })
g.Go(func() error { return work(ctx, "B", 100*time.Millisecond, true) })
g.Go(func() error { return work(ctx, "C", 500*time.Millisecond, false) })
fmt.Println("Wait returned:", g.Wait())
```
其中 `work` 里是 `select { case <-time.After(d): ...; case <-ctx.Done(): fmt.Println(name, "cancelled") }`。输出：
```
A cancelled
C cancelled
Wait returned: B failed
```
B 失败 → ctx 被取消 → A、C 在 100 毫秒时就退出，而不是等满 500 毫秒；`Wait` 返回 B 的错误。

要点：Go 的取消是**显式、协作式**的：任务必须自己监听 `ctx.Done()`；语言本身的 `go` 语句仍然是无作用域的，`errgroup` 只是一个库约定。
