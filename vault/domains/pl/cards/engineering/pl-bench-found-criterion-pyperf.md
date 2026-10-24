---
id: pl-bench-found-criterion-pyperf
node: engineering.benchmarking
type: qa
step: 4
---
## Q
Rust 的 criterion 和 Python 的 pyperf 各自怎样应对优化器和测量噪声？

## A
**Rust**：没有 JIT，不需要等编译预热，但 LLVM 优化器同样会删除无用的计算、折叠常量。标准库的 `std::hint::black_box` 是一个对优化器「不透明」的恒等函数，用它包住输入和输出，编译器就不能假设值已知或结果没用。基准必须用优化构建（`cargo bench` 默认如此），调试构建的数字没有意义。

criterion 是第三方 crate：先预热，再采集多批样本，用统计方法（自助法，bootstrap）给出置信区间，并与上一次保存的结果比较，直接判断「性能提升 / 回退 / 无显著变化」。输出里方括号依次是下界、估计值、上界：

```text
const_input   time:   [242.38 ps 243.69 ps 245.13 ps]
```

**Python**：CPython 是解释器，不存在「编译期把计算删掉」的问题，噪声来自别处：CPU 频率变化、其他进程、哈希随机化、内存布局。`timeit` 默认重复多轮并报告最小值：

```text
100000 loops, best of 5: 2.1 usec per loop
```

最小值最不受干扰，但偏乐观。`pyperf` 起多个独立的工作进程，每个进程各自预热再采样，报告均值加标准差，并检查系统是否适合做基准：

```text
Mean +- std dev: 2.13 us +- 0.05 us
```

在 Linux 上 `pyperf system tune` 还能固定 CPU 频率、隔离核心。两者的思路相同：重复、隔离、给出离散度，而不是交出一个数字。
