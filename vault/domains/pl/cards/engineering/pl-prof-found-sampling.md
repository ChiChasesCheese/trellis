---
id: pl-prof-found-sampling
node: engineering.profiling
type: qa
step: 2
---
## Q
采样剖析器（sampling profiler）是怎样工作的？读 Go `pprof` 的输出时，`flat` 和 `cum` 两列分别是什么意思？

## A
**工作方式**：启动时注册一个定时器（Go 的 CPU 剖析默认每秒 100 次，即 10 ms 一次）。每次触发，运行时记下正在 CPU 上运行的那个执行流的调用栈，给这个栈的计数加一。结束时得到一张「调用栈 → 次数」的表，次数乘以间隔就是估计的 CPU 时间。

**两个核心概念**：
- `flat`：样本的栈顶就是这个函数，即它**自己的代码**消耗的时间；
- `cum`（cumulative，累计）：这个函数出现在栈上**任何位置**的样本，即它自己加上它调用的所有函数。

**例子**：一个程序构造 20 万个字符串再排序，重复 30 轮，`go tool pprof -top` 的输出（节选）：

```text
Duration: 1.12s, Total samples = 950ms (84.85%)
      flat  flat%   sum%        cum   cum%
     230ms 24.21% 55.79%      350ms 36.84%  slices.partitionOrdered[go.shape.string]
         0     0%  1.05%      450ms 47.37%  main.sortAll (inline)
```

`main.sortAll` 的 `flat` 是 0，因为它只是转调用别的函数，但 `cum` 占 47%：整个排序阶段占了近一半。读法：找「真正耗时的代码」看 `flat`；找「该优化哪一整块工作」看 `cum`。

注意第一行：样本总量（950 ms）小于运行时长（1.12 s）。采样只发生在程序占用 CPU 时，等待不产生样本。
