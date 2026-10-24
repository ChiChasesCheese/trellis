---
id: pl-prof-pitfall-off-cpu
node: engineering.profiling
type: qa
step: 8
---
## Q
CPU 剖析显示几乎没有热点，但请求就是很慢，为什么？应该怎么办？

## A
采样器默认只在线程**占用 CPU**（on-CPU）时取样。线程在等待数据库、网络、睡眠、锁或 channel 时不产生样本，所以慢的那部分在 CPU 火焰图里根本看不见。

**例**：Go 程序顺序处理 10 次请求，每次 10 ms 计算加 90 ms 等待（`time.Sleep` 代替数据库调用），开启 CPU 剖析：

```go
func handle() {
    spin(10 * time.Millisecond)       // compute
    time.Sleep(90 * time.Millisecond) // stands in for a DB call
}
```

`go tool pprof -top` 的第二行：

```text
Duration: 1.11s, Total samples = 90ms ( 8.08%)
```

墙钟（wall-clock）时间 1.11 s，样本只覆盖 90 ms，约 92% 的时间不在图里。把计算优化到零，也只能省不到一成。

**处理**：
1. 先比较 CPU 时间与墙钟时间：占比低就是等待型，不要继续盯 CPU 火焰图。
2. 换一种能看到等待的剖析：Go 的 block、mutex 与 goroutine 剖析；Java 的 JFR 锁与 I/O 事件，或 async-profiler 的墙钟模式；Python 的 `py-spy record --idle`（把空闲线程也算进来）。
3. 请求跨越多个服务时，用分布式追踪看每个下游调用各花了多久。
