---
id: pl-conc-parallel-found-go
node: concurrency.parallelism
type: qa
step: 4
---
## Q
Go 没有标准库的并行迭代器，要对一大批数据做并行计算时怎么写？分片（sharding）模式是什么？

## A
Go 的哲学是显式：并行靠自己用 goroutine 拆。通用模式叫**分片**：
1. 按核数（`runtime.NumCPU()`）把数据范围切成 w 份；
2. 每份起一个 goroutine，只处理自己那一份，把结果写进一个**每个 goroutine 独占的槽位**（切片的不同下标）；
3. `WaitGroup` 等全部完成，再把各槽位的部分结果合并。

```go
w := runtime.NumCPU()
parts := make([]float64, w)
var wg sync.WaitGroup
for k := 0; k < w; k++ {
    wg.Go(func() { parts[k] = sum(k*n/w, (k+1)*n/w) })
}
wg.Wait()
total := 0.0
for _, p := range parts { total += p }
```
实测（1 亿个元素，`sqrt(i) * sin(i)` 求和，12 核，一次测量）：顺序 265 毫秒，12 个 goroutine 40 毫秒，约 6.6 倍。

为什么这样写是安全的：每个 goroutine 写**不同的下标**（`parts[k]`），没有两个 goroutine 写同一内存，所以不需要锁；`wg.Wait()` 建立了 happens-before，主 goroutine 读 `parts` 时一定能看到各 goroutine 的写入。

这个模式还有两个变体：
- 任务大小不均时，用 **工作队列**（一个 channel 分发小任务给固定数量的 worker）而不是静态等分；
- 需要错误传播和取消时，用 `errgroup`。

代价：样板代码多，分片、负载均衡和合并都要自己写；好处：没有隐藏的魔法，性能行为可预测。
