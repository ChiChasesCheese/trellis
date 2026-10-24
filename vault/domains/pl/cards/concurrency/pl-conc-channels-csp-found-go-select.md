---
id: pl-conc-channels-csp-found-go-select
node: concurrency.channels-csp
type: qa
step: 3
---
## Q
Go 的 `select` 语句是做什么的？怎样用它同时等待多个 channel，并实现超时？

## A
`select` 同时等待多个 channel 操作，**哪个先就绪就执行哪个分支**；多个同时就绪则随机选一个；全都没就绪就阻塞（有 `default` 分支则立即走 `default`）。它的结构像 `switch`，但每个 `case` 是一次通道收发。

心智模型：你同时盯着几个信箱，哪个先有信就先处理哪个；再放一个闹钟当“最后期限”。

超时的写法：`time.After(d)` 返回一个通道，`d` 之后会收到一个值，把它当成一个 `case`：
```go
a, b := make(chan string), make(chan string)
go func() { time.Sleep(30 * time.Millisecond); a <- "from a" }()
go func() { time.Sleep(10 * time.Millisecond); b <- "from b" }()
for i := 0; i < 2; i++ {
    select {
    case m := <-a: fmt.Println(m)
    case m := <-b: fmt.Println(m)
    case <-time.After(200 * time.Millisecond): fmt.Println("timeout")
    }
}
select {
case m := <-a: fmt.Println(m)
case <-time.After(50 * time.Millisecond): fmt.Println("timeout")
}
```
输出：`from b`、`from a`、`timeout`。前两轮谁先到先处理（b 在 10 毫秒、a 在 30 毫秒）；第三次 `a` 已经没有发送方，50 毫秒后超时分支就绪。

`select` 是 CSP 中“选择（alternation）”运算的直接实现。常用模式：
1. **多路汇聚**：同时监听多个来源；
2. **超时**：加一个 `time.After` 分支；
3. **取消**：加一个 `<-ctx.Done()` 分支，上游取消时立刻退出；
4. **非阻塞尝试**：加 `default` 分支。
