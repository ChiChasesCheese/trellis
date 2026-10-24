---
id: pl-conc-datarace-found-race-detector
node: concurrency.data-race-freedom
type: qa
step: 3
---
## Q
Go 的竞争检测器（`-race`）是什么？怎样使用，它的报告长什么样，以及 Go 运行时对 map 并发写做了什么保护？

## A
**竞争检测器**（race detector）是编译器和运行时配合的动态检测工具：用 `go run -race`、`go test -race`、`go build -race` 构建，程序运行时它记录每次内存访问，发现两个 goroutine 之间**没有同步关系**却访问同一地址、且至少一个是写，就打印报告。

最小例子（4 个 goroutine 无保护地累加同一个变量）：
```go
var n int
for i := 0; i < 4; i++ {
    wg.Go(func() { for j := 0; j < 1_000_000; j++ { n++ } })
}
wg.Wait()
```
`go run -race` 的输出（节选）：
```
WARNING: DATA RACE
Read at 0x00c000116048 by goroutine 8:
  main.main.func1()
      race.go:16 +0x38
Previous write at 0x00c000116048 by goroutine 9:
  main.main.func1()
      race.go:16 +0x48
```
报告给出：冲突的地址、两次访问各自的 goroutine、代码位置和调用栈。不加 `-race` 时程序照样运行，只是结果（比如 `1338145` 而不是 `4000000`）每次不同。

**特点**：
- 它报告的是“这一次运行中**真的发生过**的无同步冲突访问”，没执行到的路径检测不到；
- 代价大：Go 文档给出的量级是内存增加 5 到 10 倍、运行时间增加 2 到 20 倍，所以用在测试和 CI，不在生产长期开启；
- 它没有误报：报出来的都是真实的数据竞争。

**运行时的另一道保护——map 并发写**：Go 的内置 `map` 不是线程安全的，运行时在写入时检查标志位，发现另一个 goroutine 同时在写，就直接终止进程：`fatal error: concurrent map writes`。这不是 panic，无法 `recover`。它是“尽力而为”的检查，不能代替正确的同步。
