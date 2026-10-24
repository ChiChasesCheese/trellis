---
id: pl-bench-found-go
node: engineering.benchmarking
type: qa
step: 2
---
## Q
Go 的 `go test -bench` 怎样运行基准？`b.N` 循环和 Go 1.24 加入的 `b.Loop` 有什么区别？

## A
基准函数形如 `func BenchmarkX(b *testing.B)`，和单元测试放在同一个 `_test.go` 文件里。框架先用小的迭代次数 N 试跑，再不断放大 N，直到总耗时达到约 1 秒（`-benchtime` 可改），最后输出 `ns/op`（每次迭代的平均耗时）。`-benchmem` 再给出每次操作的分配字节数与次数。

**旧写法** `for i := 0; i < b.N; i++ { f(i) }`：编译器看得见整个循环体，如果 `f` 可以内联而且结果没人用，整次调用可以被当作死代码删掉。

**`b.Loop()`**（Go 1.24 起）：`for b.Loop() { f() }`。它让循环里被调用函数的参数与结果保持存活，编译器不能把调用整个优化掉；并且基准函数在每个 `-count` 里只执行一次，循环外的准备代码不会被重复执行和计时。

**同一个函数的三种写法实测**（一个 64 位整数混合函数 `mix`，Apple 芯片，一次测量）：

```go
for i := 0; i < b.N; i++ { mix(uint64(i)) }          //  0.21 ns/op
for i := 0; i < b.N; i++ { sink = mix(uint64(i)) }   //  0.46 ns/op
for i := 0; b.Loop(); i++ { mix(uint64(i)) }         //  1.26 ns/op
```

第一种丢掉结果，0.21 ns 不到一个时钟周期，是计算被整个删掉的信号；第二种把结果写到包级变量 `sink`，仍被流水线化得很快；只有第三种在测真实的开销。同一个函数，三种写法差 6 倍。
